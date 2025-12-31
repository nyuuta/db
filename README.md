# Canteen API

## Tech
FastAPI, SQLAlchemy, Alembic, PostgreSQL (Docker)

## Run
1) Start DB
docker compose up -d

2) Install deps
pip install -r requirements.txt

3) Apply migrations
alembic upgrade head

4) Run app
uvicorn app.main:app --reload

Swagger: http://127.0.0.1:8000/docs

## Seed (via REST API)
python3 scripts/seed_via_api.py

## Main endpoints
- /health
- /clients (CRUD)
- /dishes (CRUD)
- /orders (create/list/get)
- /analytics (SQL queries: WHERE/JOIN/UPDATE/GROUP BY + sorting + pagination)

