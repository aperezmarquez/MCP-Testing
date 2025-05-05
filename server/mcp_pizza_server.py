from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from data import connect_db, get_menu, create_order, close_db
from decimal import Decimal
import time

# Initialize FastMCP server
mcp = FastMCP("pizza-restaurant")

@mcp.tool()
def get_restaurant_menu():
    conn = connect_db()

    try:
        menu = get_menu(conn)
    except Exception as e:
        print(f"Error getting menu: {e}")
        menu = None

    close_db(conn)
    return menu

def add_pizza_order(pizza_order, pizza_name, pizza_size, pizza_price):
    if not pizza_order:
        pizza_order = [
            {'name': pizza_name, 'size': pizza_size, 'price': Decimal(pizza_price)}
        ]
    else:
        pizza_order.append({'name': pizza_name, 'size': pizza_size, 'price': Decimal(pizza_price)})
    
    return pizza_order

def add_drink_order(drink_order, drink_name, drink_type, drink_price):
    if not drink_order:
        drink_order = [
            {'name': drink_name, 'type': drink_type, 'price': Decimal(drink_price)}
        ]
    else:
        drink_order.append({'name': drink_name, 'type': drink_type, 'price': Decimal(drink_price)})

    return drink_order

def add_extra_order(extra_order, extra_name, extra_price):
    if not extra_order:
        extra_order = [
            {'name': extra_name, 'price': Decimal(extra_price)}
        ]
    else:
        extra_order.append({'name': extra_name, 'price': Decimal(extra_price)})

    return extra_order

@mcp.tool()
def create_final_order(pizza_name, pizza_size, pizza_price, drink_name, drink_type, drink_price, extra_name, extra_price):
    conn = connect_db()

    pizza_order = add_pizza_order(None, pizza_name, pizza_size, pizza_price)
    drink_order = add_drink_order(None, drink_name, drink_type, drink_price)
    extra_order = add_extra_order(None, extra_name, extra_price)

    try:
        order = create_order(pizza_order, drink_order, extra_order, conn)
    except Exception as e:
        print(f"Error creating order: {e}")

    close_db(conn)
    return order

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

