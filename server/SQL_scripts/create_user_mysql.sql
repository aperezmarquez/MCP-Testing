-- Create a new user
CREATE USER 'pizza_user'@'%' IDENTIFIED BY 'pass1234';

-- Grant privileges for the pizza_restaurant database
GRANT ALL PRIVILEGES ON pizza_restaurant.* TO 'pizza_user'@'%';

-- Applies all changes
FLUSH PRIVILEGES;
