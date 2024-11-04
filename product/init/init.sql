-- Tabela: products
use Product;

-- Tabela: categories
CREATE TABLE IF NOT EXISTS categories (
    categoryID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL
);

-- Tabela: statuses
CREATE TABLE IF NOT EXISTS statuses (
    statusID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS products (
    productID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL UNIQUE,
    price FLOAT NOT NULL
);
-- Tabela: orders
CREATE TABLE IF NOT EXISTS orders (
    orderID INT PRIMARY KEY AUTO_INCREMENT,
    price FLOAT NOT NULL DEFAULT 0.0,
    timestamp DATETIME NOT NULL,
    statusID INT NOT NULL,
    buyer VARCHAR(256) NOT NULL,
    FOREIGN KEY (statusID) REFERENCES statuses(statusID)
);
-- Tabela: productQuantities
CREATE TABLE IF NOT EXISTS productQuantities (
    productQuantityID INT PRIMARY KEY AUTO_INCREMENT,
    productID INT NOT NULL,
    quantity INT NOT NULL,
    orderID INT NOT NULL,
    FOREIGN KEY (productID) REFERENCES products(productID),
    FOREIGN KEY (orderID) REFERENCES orders(orderID)
);

-- Tabela: productCategories
CREATE TABLE IF NOT EXISTS productCategories (
    productCategoryId INT PRIMARY KEY AUTO_INCREMENT,
    productID INT NOT NULL,
    categoryID INT NOT NULL,
    FOREIGN KEY (productID) REFERENCES products(productID),
    FOREIGN KEY (categoryID) REFERENCES categories(categoryID)
);


INSERT INTO statuses (name)
VALUES ('CREATED'),('PENDING'), ('COMPLETE')