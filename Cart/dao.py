#Opt
import os
import sqlite3

# Use a global connection pool to reduce connection overhead
_connection_pool = None


def get_connection():
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = sqlite3.connect('products.db', check_same_thread=False)
        _connection_pool.row_factory = sqlite3.Row
        create_tables(_connection_pool)
    return _connection_pool


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            cost REAL NOT NULL,
            qty INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

    # Preload data only once (if table is empty)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('Backpack', 'A durable and stylish backpack for daily use.', 800.0, 10),
            ('Wireless Mouse', 'A sleek and ergonomic wireless mouse with a long battery life.', 800.0, 20),
            ('Bluetooth Speaker', 'A portable Bluetooth speaker with high-quality sound and deep bass.', 3000.0, 30),
            # Add remaining entries here...
        ]
        conn.executemany(
            "INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)",
            sample_products,
        )
        conn.commit()


def list_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    return [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries directly


def add_product(product: dict):
    conn = get_connection()
    conn.execute(
        'INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)',
        (product['name'], product['description'], product['cost'], product['qty']),
    )
    conn.commit()


def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    return dict(row) if row else None  # Return dict directly


def update_qty(product_id: int, qty: int):
    conn = get_connection()
    conn.execute('UPDATE products SET qty = ? WHERE id = ?', (qty, product_id))
    conn.commit()


def delete_product(product_id: int):
    conn = get_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()


def update_product(product_id: int, product: dict):
    conn = get_connection()
    conn.execute(
        'UPDATE products SET name = ?, description = ?, cost = ?, qty = ? WHERE id = ?',
        (product['name'], product['description'], product['cost'], product['qty'], product_id),
    )
    conn.commit()

#Unopt
# import os
# import sqlite3

# # Use a global connection pool to reduce connection overhead
# _connection_pool = None


# def get_connection():
#     global _connection_pool
#     if _connection_pool is None:
#         _connection_pool = sqlite3.connect('products.db', check_same_thread=False)
#         _connection_pool.row_factory = sqlite3.Row
#         create_tables(_connection_pool)
#     return _connection_pool


# def create_tables(conn):
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS products (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             description TEXT NOT NULL,
#             cost REAL NOT NULL,
#             qty INTEGER DEFAULT 0
#         )
#     ''')
#     conn.commit()

#     # Preload data only once (if table is empty)
#     cursor = conn.cursor()
#     cursor.execute('SELECT COUNT(*) FROM products')
#     if cursor.fetchone()[0] == 0:
#         sample_products = [
#             ('Backpack', 'A durable and stylish backpack for daily use.', 800.0, 10),
#             ('Wireless Mouse', 'A sleek and ergonomic wireless mouse with a long battery life.', 800.0, 20),
#             ('Bluetooth Speaker', 'A portable Bluetooth speaker with high-quality sound and deep bass.', 3000.0, 30),
#             # Add remaining entries here...
#         ]
#         conn.executemany(
#             "INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)",
#             sample_products,
#         )
#         conn.commit()


# def list_products():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM products')
#     return [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries directly


# def add_product(product: dict):
#     conn = get_connection()
#     conn.execute(
#         'INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)',
#         (product['name'], product['description'], product['cost'], product['qty']),
#     )
#     conn.commit()


# def get_product(product_id: int):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
#     row = cursor.fetchone()
#     return dict(row) if row else None  # Return dict directly


# def update_qty(product_id: int, qty: int):
#     conn = get_connection()
#     conn.execute('UPDATE products SET qty = ? WHERE id = ?', (qty, product_id))
#     conn.commit()


# def delete_product(product_id: int):
#     conn = get_connection()
#     conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
#     conn.commit()


# def update_product(product_id: int, product: dict):
#     conn = get_connection()
#     conn.execute(
#         'UPDATE products SET name = ?, description = ?, cost = ?, qty = ? WHERE id = ?',
#         (product['name'], product['description'], product['cost'], product['qty'], product_id),
#     )
#     conn.commit()
