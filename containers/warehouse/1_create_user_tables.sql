DROP SCHEMA IF EXISTS housing;
CREATE SCHEMA housing;
DROP TABLE IF EXISTS housing.user;
CREATE TABLE housing.user (
    id INT,
    price INT
);
DROP TABLE IF EXISTS housing.user_enriched;
CREATE TABLE housing.user_enriched (
    id INT,
    name VARCHAR(50),
    price INT
);