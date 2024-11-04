-- Table for storing statuses, each with a unique identifier and name
CREATE TABLE statuses (
    statusID INT PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL
);

-- Table for storing products, each with a unique identifier, name, and price
CREATE TABLE products (
    productID INT PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    price FLOAT NOT NULL
);

-- Table for storing categories, each with a unique identifier and name
CREATE TABLE categories (
    categoryID INT PRIMARY KEY,
    name VARCHAR(256) NOT NULL
);

-- Many-to-many relationship table for associating products with categories
CREATE TABLE productCategories (
    productCategoryId INT PRIMARY KEY,
    productID INT,
    categoryID INT,
    FOREIGN KEY (productID) REFERENCES products(productID),
    FOREIGN KEY (categoryID) REFERENCES categories(categoryID)
);

-- Table for storing orders, including order ID, total price, timestamp, status ID, and buyer
CREATE TABLE orders (
    orderID INT PRIMARY KEY,
    price FLOAT NOT NULL DEFAULT 0.0,
    timestamp DATETIME NOT NULL,
    statusID INT,
    buyer VARCHAR(256) NOT NULL,
    FOREIGN KEY (statusID) REFERENCES statuses(statusID)
);

-- Table for storing product quantities associated with specific orders
CREATE TABLE productQuantities (
    productQuantityID INT PRIMARY KEY,
    productID INT,
    quantity INT NOT NULL,
    orderID INT,
    FOREIGN KEY (productID) REFERENCES products(productID),
    FOREIGN KEY (orderID) REFERENCES orders(orderID)
);

