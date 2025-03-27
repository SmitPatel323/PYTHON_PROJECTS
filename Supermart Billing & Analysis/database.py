import sqlite3
import bcrypt


def init_db():
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        barcode TEXT PRIMARY KEY,
                        name TEXT,
                        price REAL,
                        stock INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        items TEXT,
                        total_price REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS product_sale (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        barcode TEXT,
                        name TEXT,
                        date date DEFAULT CURRENT_DATE,
                        total_sales INTEGER)''')

    conn.commit()
    conn.close()


def insert_default_products():
    products = [
        ("8901765126207", "BallPen", 2.5, 100),
        ("8901057510028", "Staples", 1.8, 80),
        ("8901571006854", "ENO", 7.8, 30),
        ("8901262010320", "Amul Butter", 1.2, 90),
        ("357159852", "Shampoo", 4.5, 70),
        ("852741963", "Toothpaste", 3.0, 50),
        ("147258369", "Coffee (250g)", 6.0, 35),
        ("23002170110130","Stud",1,2),
        ("9780062273208","Book",10,5),
        ("1H123B277418","mysy",5,1),
        ("8904089803021","sunscreen",10,2)
    ]

    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()

    for product in products:
        cursor.execute("INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)", product)

    conn.commit()
    conn.close()

def get_product(barcode):
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
    product = cursor.fetchone()
    conn.close()
    return product

def get_all_products():
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def update_stock(barcode, quantity):
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock = stock - ? WHERE barcode = ?", (quantity, barcode))
    conn.commit()
    conn.close()

def record_sale(date, items, total_price):
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sales (date, items, total_price) VALUES (?, ?, ?)",
                   (date, str(items), total_price))
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    stored_password = cursor.fetchone()
    conn.close()
    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
        return True
    return False

def insert_product(barcode, name, price, stock):
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)", (barcode, name, price, stock))
    cursor.execute("UPDATE products SET stock = stock + ? WHERE barcode = ?", (stock, barcode))
    conn.commit()
    conn.close()

def product_sales(barcode,name,total_sales):
    conn = sqlite3.connect("supermart.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product_sale (barcode,name,total_sales) VALUES (?,?,?)",(barcode,name,total_sales))
    conn.commit()

init_db()
insert_default_products()
