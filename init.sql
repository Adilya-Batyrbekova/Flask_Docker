CREATE DATABASE counterdb;

\c counterdb;

CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    client_info TEXT NOT NULL
);
