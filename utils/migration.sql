CREATE DATABASE IF NOT EXISTS criptochat;

USE criptochat;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL
);

INSERT INTO user (username, password)
VALUES ("pokemon", "platinum");