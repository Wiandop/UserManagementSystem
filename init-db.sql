-- Creation of the database schema and initial data for a user management system

-- Creation of the users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    money_amount REAL NOT NULL,
    card_number TEXT NOT NULL,
    status BIT NOT NULL
);

-- Creation of the users_passwords table
CREATE TABLE IF NOT EXISTS users_passwords (
    user_id INTEGER PRIMARY KEY,
    password TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

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