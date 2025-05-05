import mysql.connector
import json
from decimal import Decimal
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=db_name
    )
    return conn

def close_db(conn):
    cursor = conn.cursor()

    # Close connection
    cursor.close()
    conn.close()

# Convert Decimal to float or str for JSON serialization
def decimal_converter(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # or str(obj) if you need precision
    raise TypeError("Type not serializable")

def select_all(table, conn):
    cursor.execute(f"SELECT * FROM {table}")

    # Fetch all rows
    rows = cursor.fetchall()

    # Column names (use these to convert into JSON format)
    columns = [desc[0] for desc in cursor.description]

    # Convert rows to list of dictionaries
    result = []
    for row in rows:
        row_dict = {columns[i]: row[i] for i in range(len(row))}
        result.append(row_dict)

    # Convert to JSON
    json_result = json.dumps(result, default=decimal_converter)

    return json_result

def get_menu(conn):
    menu = []
    
    menu.append({ 'pizzas': select_all("pizzas", conn)})
    menu.append({ 'tamanos_pizza': select_all("tamanos", conn)})
    menu.append({ 'extras': select_all("extras", conn)})
    menu.append({ 'bebidas': select_all("bebidas", conn)})

    return menu

def get_orders(conn):
    orders = []

    orders.append({ 'orders': select_all("orders", conn)})
    orders.append({ 'order_pizzas': select_all("pizzas_ordered", conn)})
    orders.append({ 'order_bebidas': select_all("drinks_ordered", conn)})
    orders.append({ 'order_extras': select_all("extras_ordered", conn)})

    return orders

def create_order(pizza_order, drink_order, extra_order, conn):
    cursor = conn.cursor()

    try:
        # Insert into the 'orders' table
        cursor.execute("INSERT INTO orders (order_date) VALUES (CURRENT_TIMESTAMP)")
        conn.commit()  # Commit to get the order_id

        # Get the order_id of the inserted order
        order_id = cursor.lastrowid

        # Insert into 'pizzas_ordered' table
        for pizza in pizza_order:
            cursor.execute("""
                INSERT INTO pizzas_ordered (order_id, pizza_name, pizza_size, pizza_price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, pizza['name'], pizza['size'], pizza['price']))
        
        # Insert into 'drinks_ordered' table
        for drink in drink_order:
            cursor.execute("""
                INSERT INTO drinks_ordered (order_id, drink_name, drink_type, drink_price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, drink['name'], drink['type'], drink['price']))
        
        # Insert into 'extras_ordered' table
        for extra in extra_order:
            cursor.execute("""
                INSERT INTO extras_ordered (order_id, extra_name, extra_price)
                VALUES (%s, %s, %s)
            """, (order_id, extra['name'], extra['price']))

        # Commit all changes
        conn.commit()

        print("Order successfully added!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # Rollback if any error occurs
