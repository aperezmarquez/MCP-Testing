-- Use the pizza_restaurant database
USE pizza_restaurant;

-- Drops tables if exist
DROP TABLE IF EXISTS pizzas_ordered;
DROP TABLE IF EXISTS drinks_ordered;
DROP TABLE IF EXISTS extras_ordered;
DROP TABLE IF EXISTS orders;

-- Create table for storing orders
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,  -- Use AUTO_INCREMENT for MySQL
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for ordered pizzas
CREATE TABLE pizzas_ordered (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use AUTO_INCREMENT for MySQL
    order_id INT NOT NULL,
    pizza_name VARCHAR(50) NOT NULL,
    pizza_size VARCHAR(20),
    pizza_price DECIMAL(5,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

-- Create table for ordered drinks
CREATE TABLE drinks_ordered (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use AUTO_INCREMENT for MySQL
    order_id INT NOT NULL,
    drink_name VARCHAR(50) NOT NULL,
    drink_type VARCHAR(20),
    drink_price DECIMAL(5,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

-- Create table for ordered extras
CREATE TABLE extras_ordered (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Use AUTO_INCREMENT for MySQL
    order_id INT NOT NULL,
    extra_name VARCHAR(50) NOT NULL,
    extra_price DECIMAL(5,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);
