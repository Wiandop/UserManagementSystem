-- Creation of the database and initial data for a user management system
CREATE DATABASE IF NOT EXISTS app;
USE app;

-- Creation of the users table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(255) NOT NULL UNIQUE,
    money_amount DECIMAL(12, 2) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    status TINYINT(1) NOT NULL
) ENGINE=InnoDB;

-- Creation of the users_passwords table
DROP TABLE IF EXISTS users_passwords;
CREATE TABLE users_passwords (
    user_id INT PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- Inserting initial data into the users table
INSERT INTO users (login, money_amount, card_number, status) VALUES
('admin', 1000000.01, '341400659026034', 1),
('Richard Pryce', 2.75, '372948584215422', 1),
('Albert Gonzalez', 800.00, '343684895953560', 1),
('Adrian Lamo', 6543.21, '3560997692591558', 0),
('Kevin Mitnick', 1234.56, '4101621005948372', 0);

-- Inserting initial data into the users_passwords table
INSERT INTO users_passwords (user_id, password) VALUES
(1, 'password'),
(2, '12345678'),
(3, 'qwerty'),
(4, '00000000'),
(5, 'passpass');