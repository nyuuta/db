from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.db import get_db
from app.models import Dish
from app.schemas import DishCreate, DishUpdate, DishOut

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.post("", response_model=DishOut)
def create_dish(payload: DishCreate, db: Session = Depends(get_db)):
    dish = Dish(**payload.model_dump())
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


@router.get("", response_model=list[DishOut])
def list_dishes(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("id"),
    sort_dir: str = Query("asc"),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    category: Optional[str] = None,
):
    q = db.query(Dish)

 
    if min_price is not None:
        q = q.filter(Dish.price >= min_price)
    if max_price is not None:
        q = q.filter(Dish.price <= max_price)
    if category is not None:
        q = q.filter(Dish.category == category)

   
    allowed = {"id": Dish.id, "price": Dish.price, "name": Dish.name, "calories": Dish.calories}
    sort_col = allowed.get(sort_by, Dish.id)
    q = q.order_by(desc(sort_col) if sort_dir.lower() == "desc" else asc(sort_col))

    return q.offset(offset).limit(limit).all()


@router.get("/{dish_id}", response_model=DishOut)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@router.patch("/{dish_id}", response_model=DishOut)
def update_dish(dish_id: int, payload: DishUpdate, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(dish, k, v)

    db.commit()
    db.refresh(dish)
    return dish


@router.delete("/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()
    return {"deleted": True, "id": dish_id}
