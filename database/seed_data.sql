-- Sample data for Pizza Management System
-- Run this after creating the schema to populate with sample records

-- Insert sample customers
INSERT INTO customer (name, phone, email) VALUES
('John Smith', '555-0101', 'john.smith@email.com'),
('Jane Doe', '555-0102', 'jane.doe@email.com'),
('Michael Johnson', '555-0103', 'michael.j@email.com'),
('Sarah Williams', '555-0104', 'sarah.w@email.com'),
('David Brown', '555-0105', 'david.brown@email.com');

-- Insert sample pizzas
INSERT INTO pizza (name, size, price, cost) VALUES
('Margherita', 'Small', 8.99, 3.50),
('Margherita', 'Medium', 12.99, 5.00),
('Margherita', 'Large', 16.99, 6.50),
('Pepperoni', 'Small', 9.99, 4.00),
('Pepperoni', 'Medium', 13.99, 5.50),
('Pepperoni', 'Large', 17.99, 7.00),
('Vegetarian', 'Small', 10.99, 4.50),
('Vegetarian', 'Medium', 14.99, 6.00),
('Vegetarian', 'Large', 18.99, 7.50),
('Hawaiian', 'Small', 10.99, 4.50),
('Hawaiian', 'Medium', 14.99, 6.00),
('Hawaiian', 'Large', 18.99, 7.50),
('Meat Lovers', 'Small', 12.99, 5.50),
('Meat Lovers', 'Medium', 16.99, 7.00),
('Meat Lovers', 'Large', 20.99, 8.50);

-- Insert sample employees
INSERT INTO employee (username, first_name, last_name, password) VALUES
('admin', 'Admin', 'User', 'admin123'),
('jsmith', 'John', 'Smith', 'password123'),
('mdavis', 'Mary', 'Davis', 'password123'),
('rjones', 'Robert', 'Jones', 'password123');

-- Insert sample orders
INSERT INTO `order` (customer_id, date) VALUES
(1, '2025-10-20'),
(2, '2025-10-20'),
(3, '2025-10-21'),
(1, '2025-10-21'),
(4, '2025-10-22');

-- Insert sample order details
INSERT INTO order_detail (order_id, pizza_id, quantity) VALUES
(1, 2, 1),  -- Order 1: 1 Medium Margherita
(1, 5, 1),  -- Order 1: 1 Medium Pepperoni
(2, 6, 2),  -- Order 2: 2 Large Pepperoni
(3, 8, 1),  -- Order 3: 1 Medium Vegetarian
(3, 11, 1), -- Order 3: 1 Medium Hawaiian
(4, 15, 1), -- Order 4: 1 Large Meat Lovers
(5, 1, 3),  -- Order 5: 3 Small Margherita
(5, 4, 2);  -- Order 5: 2 Small Pepperoni
