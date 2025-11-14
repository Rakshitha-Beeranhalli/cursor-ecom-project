import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("ecommerce.db")
CSV_DIR = Path(".")

TABLE_SCHEMAS = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            signup_date TEXT NOT NULL
        )
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """,
    "payments": """
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            method TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """,
}

CSV_CONFIG = [
    ("users.csv", "users"),
    ("products.csv", "products"),
    ("orders.csv", "orders"),
    ("order_items.csv", "order_items"),
    ("payments.csv", "payments"),
]


def load_csv_to_table(cursor, csv_file, table_name):
    file_path = CSV_DIR / csv_file
    with file_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return

    columns = reader.fieldnames
    placeholders = ",".join(["?" for _ in columns])
    insert_sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

    converted_rows = []
    for row in rows:
        converted = []
        for col in columns:
            value = row[col]
            if value.isdigit():
                converted.append(int(value))
            else:
                try:
                    converted.append(float(value))
                except ValueError:
                    converted.append(value)
        converted_rows.append(tuple(converted))

    cursor.executemany(insert_sql, converted_rows)


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        for schema_sql in TABLE_SCHEMAS.values():
            cur.execute(schema_sql)

        for csv_file, table_name in CSV_CONFIG:
            load_csv_to_table(cur, csv_file, table_name)

        conn.commit()


if __name__ == "__main__":
    main()
