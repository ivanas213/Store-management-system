USE User;  -- Selects the 'User' database

-- Creates the 'users' table to store user details
CREATE TABLE IF NOT EXISTS users (
	userID	INTEGER AUTO_INCREMENT,           -- Unique identifier for each user
	email	    VARCHAR(256) UNIQUE,            -- User's email, must be unique
    `password`  VARCHAR(256) NOT NULL,         -- User's password, required
	forename	VARCHAR(256) NOT NULL,          -- User's first name, required
    surname	    VARCHAR(256) NOT NULL,          -- User's last name, required
	PRIMARY KEY(userID)                        -- Sets userID as the primary key
);

-- Creates the 'roles' table to define different user roles
CREATE TABLE IF NOT EXISTS roles(
	roleId INTEGER AUTO_INCREMENT,             -- Unique identifier for each role
	`name` VARCHAR(256) NOT NULL,              -- Role name, required
	PRIMARY KEY(roleID)                        -- Sets roleID as the primary key
);

-- Creates the 'userroles' table to associate users with roles
CREATE TABLE IF NOT EXISTS userroles(
	userRoleId INTEGER AUTO_INCREMENT,         -- Unique identifier for each user-role relationship
	userID INTEGER NOT NULL REFERENCES users(userID),  -- References userID from 'users' table
	roleId INTEGER NOT NULL REFERENCES roles(roleId),  -- References roleId from 'roles' table
	PRIMARY KEY(userRoleId)                    -- Sets userRoleId as the primary key
);

-- Inserts predefined roles into the 'roles' table
INSERT INTO roles(
	`name`
) values 
("customer"),("courier"),("owner");

-- Inserts a sample user into the 'users' table
INSERT INTO users (email, password, forename, surname) 
VALUES ('onlymoney@gmail.com', 'evenmoremoney', 'Scrooge', 'McDuck');

-- Assigns a role to the sample user in the 'userroles' table
INSERT INTO userroles (userID, roleID)
VALUES (1, 3);  -- Assigns 'owner' role to the user with userID 1
