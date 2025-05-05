-- Create the database
CREATE DATABASE IF NOT EXISTS pizza_restaurant;

-- Use the new database
USE pizza_restaurant;

-- Create tables
CREATE TABLE pizzas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(5,2) NOT NULL
);

CREATE TABLE tamanos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

CREATE TABLE bebidas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    lata DECIMAL(5,2),
    botella DECIMAL(5,2)
);

CREATE TABLE extras (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(5,2) NOT NULL
);

-- Insert data into pizzas
INSERT INTO pizzas (nombre, precio) VALUES
('Margarita', 8.0),
('Pepperoni', 9.5),
('Hawaiana', 10.0),
('Cuatro Quesos', 10.5);

-- Insert data into tamanos
INSERT INTO tamanos (nombre) VALUES
('pequeña'),
('mediana'),
('grande');

-- Insert data into bebidas
INSERT INTO bebidas (nombre, lata, botella) VALUES
('Coca-Cola', 1.5, 2.5),
('Agua', 1.0, 2.0),
('Fanta', 1.5, 2.5);

-- Insert data into extras
INSERT INTO extras (nombre, precio) VALUES
('extra queso', 1.0),
('salsa picante', 0.5),
('aceitunas', 0.75),
('champiñones', 0.75);
