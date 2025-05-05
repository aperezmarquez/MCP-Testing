from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from data import connect_db, get_menu, create_order, close_db

# Initialize FastMCP server
mcp = FastMCP("pizza-restaurant")

@mcp.tool()
async def get_restaurant_menu():
    try:
        conn = await connect_db()
    except Exception as e:
        print(f"Error connecting to database: {e}")

    try:
        menu = await get_menu(conn)
    except Exception as e:
        print(f"Error getting menu: {e}")
        menu = None

    await close_db(conn)
    return menu

@mcp.tool()
def add_pizza_order(pizza_order, pizza_name, pizza_size, pizza_price):
    if not pizza_order:
        pizza_order = [
            {'name': pizza_name, 'size': pizza_size, 'price': Decimal(pizza_price)}
        ]
    else:
        pizza_order.append({'name': pizza_name, 'size': pizza_size, 'price': Decimal(pizza_price)})
    
    return pizza_order

@mcp.tool()
def add_drink_order(drink_order, drink_name, drink_type, drink_price):
    if not drink_order:
        drink_order = [
            {'name': drink_name, 'type': drink_type, 'price': Decimal(drink_price)}}
        ]
    else:
        drink_order.append({'name': drink_name, 'type': drink_type, 'price': Decimal(drink_price)})

    return drink_order

@mcp.tool()
def add_extra_order(extra_order, extra_name, extra_price):
    if not extra_order:
        extra_order = [
            {'name': extra_name, 'price': Decimal(extra_price)}
        ]
    else:
        extra_order.append({'name': extra_name, 'price': Decimal(extra_price)})

    return extra_order

@mcp.tool()
async def create_order(pizza_order, drink_order, extra_order):
    try:
        conn = await connect_db()
    except Exception as e:
        print(f"Error connecting to database: {e}")
    
    try:
        order = await create_order(pizza_order, drink_order, extra_order, conn)
    except Exception as e:
        print(f"Error creating order: {e}")

    await close_db(conn)
    return order
