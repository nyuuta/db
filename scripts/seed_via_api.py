import random
import requests

BASE_URL = "http://127.0.0.1:8000"

# ---------- helpers ----------

def post(path, data):
    r = requests.post(f"{BASE_URL}{path}", json=data)
    r.raise_for_status()
    return r.json()

def get(path):
    r = requests.get(f"{BASE_URL}{path}")
    r.raise_for_status()
    return r.json()


# ---------- seed dishes ----------

def seed_dishes(n=50):
    print(f"Seeding {n} dishes...")
    dish_ids = []

    categories = ["soup", "main", "dessert", "drink"]

    for i in range(n):
        payload = {
            "name": f"dish_{i}",
            "price": random.randint(500, 3000),
            "calories": random.randint(100, 900),
            "portion_grams": random.randint(150, 500),
            "category": random.choice(categories),
            "meta": {
                "tags": ["seed", "auto"],
                "rating": random.randint(1, 5),
            },
        }
        dish = post("/dishes", payload)
        dish_ids.append(dish["id"])

    return dish_ids


# ---------- seed clients ----------

def seed_clients(n=30):
    print(f"Seeding {n} clients...")
    client_ids = []

    for i in range(n):
        payload = {
            "full_name": f"Client {i}",
            "age": random.randint(18, 65),
            "weight_kg": random.randint(50, 100),
            "organization": "YSU",
            "preferences": "seed data",
        }
        client = post("/clients", payload)
        client_ids.append(client["id"])

    return client_ids


# ---------- seed orders ----------
def seed_orders(client_ids, dish_ids, n=100):
    print(f"Seeding {n} orders...")

    for _ in range(n):
        # выбираем уникальные блюда для заказа
        chosen_dishes = random.sample(dish_ids, k=random.randint(1, min(4, len(dish_ids))))

        items = []
        for dish_id in chosen_dishes:
            items.append(
                {
                    "dish_id": dish_id,
                    "quantity": random.randint(1, 3),
                }
            )

        payload = {
            "client_id": random.choice(client_ids),
            "payment_type": random.choice(["cash", "card"]),
            "items": items,
        }

        post("/orders", payload)




if __name__ == "__main__":
    print("START SEED")

    dishes = seed_dishes(50)
    clients = seed_clients(30)
    seed_orders(clients, dishes, 100)

    print("SEED DONE")
