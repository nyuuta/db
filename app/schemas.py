from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class DishCreate(BaseModel):
    name: str
    price: float
    calories: Optional[int] = None
    portion_grams: Optional[int] = None
    category: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class DishUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    portion_grams: Optional[int] = None
    category: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class DishOut(BaseModel):
    id: int
    name: str
    price: float
    calories: Optional[int] = None
    portion_grams: Optional[int] = None
    category: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True



class ClientCreate(BaseModel):
    full_name: str
    age: Optional[int] = None
    weight_kg: Optional[int] = None
    organization: Optional[str] = None
    preferences: Optional[str] = None


class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    weight_kg: Optional[int] = None
    organization: Optional[str] = None
    preferences: Optional[str] = None


class ClientOut(BaseModel):
    id: int
    full_name: str
    age: Optional[int] = None
    weight_kg: Optional[int] = None
    organization: Optional[str] = None
    preferences: Optional[str] = None

    class Config:
        from_attributes = True



class OrderItemCreate(BaseModel):
    dish_id: int
    quantity: int


class OrderCreate(BaseModel):
    client_id: int
    payment_type: Optional[str] = None
    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    dish_id: int
    quantity: int

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    client_id: int
    payment_type: Optional[str] = None
    created_at: Optional[str] = None
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
