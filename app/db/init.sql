-- Drop and recreate DB (optional)
DROP DATABASE IF EXISTS rbac_demo;
CREATE DATABASE rbac_demo;
USE rbac_demo;

-- =========================
-- TABLES
-- =========================

CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(100),
  role VARCHAR(20)
);

CREATE TABLE vendors (
  id INT PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE products (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  price DECIMAL(10,2),
  cost_price DECIMAL(10,2),
  vendor_id INT
);

CREATE TABLE orders (
  id INT PRIMARY KEY,
  user_id INT,
  total_amount DECIMAL(10,2),
  status VARCHAR(20)
);

CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT,
  product_id INT,
  quantity INT,
  price DECIMAL(10,2)
);

CREATE TABLE payments (
  id INT PRIMARY KEY,
  order_id INT,
  amount DECIMAL(10,2),
  method VARCHAR(20),
  card_last4 VARCHAR(4),
  status VARCHAR(20)
);

-- =========================
-- SEED DATA
-- =========================

INSERT INTO users VALUES
(1, 'admin@test.com', 'admin'),
(2, 'vendor1@test.com', 'vendor'),
(3, 'buyer1@test.com', 'buyer');

INSERT INTO vendors VALUES
(1, 'Nike'),
(2, 'Adidas');

INSERT INTO products VALUES
(1, 'Shoes', 5000, 3000, 1),
(2, 'T-Shirt', 2000, 1000, 2);

INSERT INTO orders VALUES
(1, 3, 7000, 'completed'),
(2, 3, 2000, 'pending');

INSERT INTO order_items VALUES
(1, 1, 1, 1, 5000),
(2, 1, 2, 1, 2000);

INSERT INTO payments VALUES
(1, 1, 7000, 'card', '1234', 'paid');