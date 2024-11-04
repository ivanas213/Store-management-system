-- Table for storing user details
CREATE TABLE users (
    userID INT PRIMARY KEY,           -- Unique ID for each user
    forename VARCHAR(256) NOT NULL,    -- User's first name, cannot be NULL
    lastname VARCHAR(256) NOT NULL,    -- User's last name, cannot be NULL
    email VARCHAR(256) UNIQUE,         -- User's email, must be unique
    password VARCHAR(256)              -- User's password
);

-- Table for storing role details
CREATE TABLE roles (
    roleID INT PRIMARY KEY,            -- Unique ID for each role
    name VARCHAR(256) NOT NULL         -- Role name, cannot be NULL
);

-- Junction table linking users and roles for a many-to-many relationship
CREATE TABLE userRoles (
    userRoleId INT PRIMARY KEY,        -- Unique ID for each user-role relation
    userID INT,                        -- References userID in users table
    roleID INT,                        -- References roleID in roles table
    FOREIGN KEY (userID) REFERENCES users(userID),  -- Foreign key constraint to users table
    FOREIGN KEY (roleID) REFERENCES roles(roleID)   -- Foreign key constraint to roles table
);
