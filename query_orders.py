import sqlite3
from pathlib import Path

DB_PATH = Path("ecommerce.db")

QUERY = """
SELECT
    u.first_name || ' ' || u.last_name AS user_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price AS price,
    o.total_amount,
    o.order_date,
    pay.status AS payment_status
FROM orders AS o
JOIN users AS u ON o.user_id = u.user_id
JOIN order_items AS oi ON o.order_id = oi.order_id
JOIN products AS p ON oi.product_id = p.product_id
JOIN payments AS pay ON o.order_id = pay.order_id
ORDER BY o.order_date, o.order_id;
"""


def print_table(rows, headers):
    widths = [len(h) for h in headers]
    for row in rows:
        for idx, value in enumerate(row):
            value_str = str(value)
            widths[idx] = max(widths[idx], len(value_str))

    divider = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    header_row = "|" + "|".join(f" {headers[i].ljust(widths[i])} " for i in range(len(headers))) + "|"

    print(divider)
    print(header_row)
    print(divider)

    for row in rows:
        print("|" + "|".join(f" {str(row[i]).ljust(widths[i])} " for i in range(len(row))) + "|")
    print(divider)


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(QUERY)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]

    print_table(rows, headers)


if __name__ == "__main__":
    main()
