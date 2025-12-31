from fastapi import FastAPI

from app.routers.dishes import router as dishes_router
from app.routers.clients import router as clients_router
from app.routers.orders import router as orders_router
from app.routers.analytics import router as analytics_router
app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(dishes_router)
app.include_router(clients_router)
app.include_router(orders_router)
app.include_router(analytics_router)
