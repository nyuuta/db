from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dishes/filter_sql")
def dishes_filter_sql(
    db: Session = Depends(get_db),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_calories: Optional[int] = None,
    category: Optional[str] = None,
    sort_by: str = Query("id"),
    sort_dir: str = Query("asc"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    allowed_sort = {"id", "price", "name", "calories"}
    if sort_by not in allowed_sort:
        sort_by = "id"
    sort_dir = "desc" if sort_dir.lower() == "desc" else "asc"

    sql = text(f"""
        SELECT id, name, price, calories, portion_grams, category, meta
        FROM dishes
        WHERE (:min_price IS NULL OR price >= :min_price)
          AND (:max_price IS NULL OR price <= :max_price)
          AND (:min_calories IS NULL OR calories >= :min_calories)
          AND (:category IS NULL OR category = :category)
        ORDER BY {sort_by} {sort_dir}
        LIMIT :limit OFFSET :offset
    """)

    rows = db.execute(
        sql,
        {
            "min_price": min_price,
            "max_price": max_price,
            "min_calories": min_calories,
            "category": category,
            "limit": limit,
            "offset": offset,
        },
    ).fetchall()

    return [dict(r._mapping) for r in rows]


@router.get("/clients/{client_id}/orders_sql")
def client_orders_sql(client_id: int, db: Session = Depends(get_db)):
    sql = text("""
        SELECT
          o.id AS order_id,
          o.created_at,
          o.payment_type,
          SUM(d.price * oi.quantity) AS total_sum
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        JOIN dishes d ON d.id = oi.dish_id
        WHERE o.client_id = :client_id
        GROUP BY o.id, o.created_at, o.payment_type
        ORDER BY o.id DESC
    """)

    rows = db.execute(sql, {"client_id": client_id}).fetchall()
    return [dict(r._mapping) for r in rows]


@router.post("/dishes/raise_price_sql")
def raise_price_sql(
    category: str = Query(...),
    min_calories: int = Query(0),
    percent: float = Query(10.0),
    db: Session = Depends(get_db),
):
    multiplier = 1.0 + percent / 100.0

    sql = text("""
        UPDATE dishes
        SET price = price * :multiplier
        WHERE category = :category
          AND calories >= :min_calories
    """)

    res = db.execute(
        sql,
        {
            "multiplier": multiplier,
            "category": category,
            "min_calories": min_calories,
        },
    )
    db.commit()
    return {"updated": res.rowcount, "category": category, "percent": percent}


@router.get("/top_clients_by_spend_sql")
def top_clients_by_spend_sql(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
):
    sql = text("""
        SELECT
          c.id AS client_id,
          c.full_name,
          SUM(d.price * oi.quantity) AS total_spend
        FROM clients c
        JOIN orders o ON o.client_id = c.id
        JOIN order_items oi ON oi.order_id = o.id
        JOIN dishes d ON d.id = oi.dish_id
        GROUP BY c.id, c.full_name
        ORDER BY total_spend DESC
        LIMIT :limit
    """)

    rows = db.execute(sql, {"limit": limit}).fetchall()
    return [dict(r._mapping) for r in rows]

@router.get("/orders/{order_id}/full_sql")
def order_full_sql(order_id: int, db: Session = Depends(get_db)):
    sql = text("""
        SELECT
          o.id AS order_id,
          o.created_at,
          o.payment_type,
          c.id AS client_id,
          c.full_name,
          oi.dish_id,
          d.name AS dish_name,
          d.price AS dish_price,
          oi.quantity,
          (d.price * oi.quantity) AS line_sum
        FROM orders o
        JOIN clients c ON c.id = o.client_id
        JOIN order_items oi ON oi.order_id = o.id
        JOIN dishes d ON d.id = oi.dish_id
        WHERE o.id = :order_id
        ORDER BY oi.dish_id
    """)

    rows = db.execute(sql, {"order_id": order_id}).fetchall()
    if not rows:
        return {"detail": "Order not found"}

    items = []
    total = 0.0
    for r in rows:
        m = dict(r._mapping)
        items.append(
            {
                "dish_id": m["dish_id"],
                "dish_name": m["dish_name"],
                "dish_price": float(m["dish_price"]) if m["dish_price"] is not None else 0.0,
                "quantity": m["quantity"],
                "line_sum": float(m["line_sum"]) if m["line_sum"] is not None else 0.0,
            }
        )
        total += float(m["line_sum"]) if m["line_sum"] is not None else 0.0

    first = dict(rows[0]._mapping)
    return {
        "order_id": first["order_id"],
        "created_at": str(first["created_at"]),
        "payment_type": first["payment_type"],
        "client": {"client_id": first["client_id"], "full_name": first["full_name"]},
        "items": items,
        "total_sum": total,
        }
