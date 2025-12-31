from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.models import Order, OrderItem, Client, Dish
from app.schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    # проверим клиента
    client = db.query(Client).filter(Client.id == payload.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must have items")

  
    order = Order(client_id=payload.client_id, payment_type=payload.payment_type)
    db.add(order)
    db.flush()  # получаем order.id без commit

    for item in payload.items:
        dish = db.query(Dish).filter(Dish.id == item.dish_id).first()
        if not dish:
            raise HTTPException(status_code=404, detail=f"Dish not found: {item.dish_id}")

        oi = OrderItem(order_id=order.id, dish_id=item.dish_id, quantity=item.quantity)
        db.add(oi)

    db.commit()
    db.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    # JOIN: orders -> order_items
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    orders = (
        db.query(Order)
        .options(joinedload(Order.items))
        .order_by(Order.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return orders
