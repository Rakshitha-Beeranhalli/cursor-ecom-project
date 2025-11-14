import csv
from datetime import date, timedelta

first_names = ["Ava", "Liam", "Noah", "Emma", "Olivia", "Mia", "Ethan", "Sophia", "James", "Isabella", "Lucas", "Charlotte", "Mason", "Amelia", "Logan", "Harper", "Elijah", "Evelyn", "Henry", "Abigail"]
last_names = ["Hill", "Rivera", "Chen", "Patel", "Johnson", "Garcia", "Nguyen", "Baker", "Carter", "Diaz", "Lopez", "Kim", "Clark", "Scott", "Turner", "Adams", "Brooks", "Ward", "Young", "Perez"]

users = []
base_signup = date(2023, 8, 1)
for i in range(20):
    fn = first_names[i % len(first_names)]
    ln = last_names[(i * 3) % len(last_names)]
    users.append({
        "user_id": i + 1,
        "first_name": fn,
        "last_name": ln,
        "email": f"{fn.lower()}.{ln.lower()}{i + 1}@example.com",
        "signup_date": (base_signup + timedelta(days=i * 5)).isoformat()
    })

product_specs = [
    ("Eco Water Bottle", "Home", 19.99, 120),
    ("Smart Fitness Band", "Electronics", 59.99, 80),
    ("Noise Cancelling Headphones", "Electronics", 129.5, 60),
    ("UltraSoft Hoodie", "Apparel", 48.0, 90),
    ("Minimalist Backpack", "Accessories", 72.25, 110),
    ("Bamboo Cutting Board", "Home", 24.99, 150),
    ("Ceramic Planter", "Garden", 35.5, 75),
    ("LED Desk Lamp", "Home Office", 42.0, 95),
    ("Wireless Charger Pad", "Electronics", 28.75, 130),
    ("Stainless Travel Mug", "Home", 21.5, 160),
    ("Organic Cotton Sheets", "Home", 89.99, 50),
    ("Aromatherapy Diffuser", "Wellness", 34.5, 85),
    ("Yoga Starter Kit", "Wellness", 64.0, 70),
    ("Portable Blender", "Kitchen", 54.99, 65),
    ("Bluetooth Speaker", "Electronics", 79.0, 100),
    ("Leather Journal", "Office", 26.5, 140),
    ("Scented Candle Set", "Home", 31.75, 120),
    ("Gaming Mouse", "Electronics", 49.99, 75),
    ("Trail Running Shoes", "Apparel", 92.5, 55),
    ("Insulated Picnic Tote", "Outdoors", 44.0, 105)
]

products = []
for i, (name, category, price, stock) in enumerate(product_specs, start=1):
    products.append({
        "product_id": i,
        "name": name,
        "category": category,
        "price": f"{price:.2f}",
        "stock": stock
    })

orders = []
order_items = []
payments = []
order_statuses = ["processing", "shipped", "delivered", "delivered", "cancelled"]
payment_methods = ["credit_card", "paypal", "apple_pay", "google_pay"]
order_base = date(2024, 3, 1)

for i in range(20):
    order_id = i + 1
    user_id = (i * 2) % 20 + 1
    product = products[(i * 3) % len(products)]
    quantity = (i % 3) + 1
    unit_price = float(product["price"])
    total_amount = round(quantity * unit_price, 2)
    status = order_statuses[i % len(order_statuses)]
    order_date = (order_base + timedelta(days=i)).isoformat()

    orders.append({
        "order_id": order_id,
        "user_id": user_id,
        "order_date": order_date,
        "status": status,
        "total_amount": f"{total_amount:.2f}"
    })

    order_items.append({
        "order_item_id": order_id,
        "order_id": order_id,
        "product_id": product["product_id"],
        "quantity": quantity,
        "unit_price": f"{unit_price:.2f}"
    })

    payment_status = "completed" if status != "cancelled" else "refunded"
    payment_date = (order_base + timedelta(days=i + 1)).isoformat()
    if status == "cancelled":
        payment_date = (order_base + timedelta(days=i + 2)).isoformat()

    payments.append({
        "payment_id": order_id,
        "order_id": order_id,
        "payment_date": payment_date,
        "method": payment_methods[i % len(payment_methods)],
        "amount": f"{total_amount:.2f}",
        "status": payment_status
    })

files = [
    ("users.csv", ["user_id", "first_name", "last_name", "email", "signup_date"], users),
    ("products.csv", ["product_id", "name", "category", "price", "stock"], products),
    ("orders.csv", ["order_id", "user_id", "order_date", "status", "total_amount"], orders),
    ("order_items.csv", ["order_item_id", "order_id", "product_id", "quantity", "unit_price"], order_items),
    ("payments.csv", ["payment_id", "order_id", "payment_date", "method", "amount", "status"], payments)
]

for filename, headers, rows in files:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
