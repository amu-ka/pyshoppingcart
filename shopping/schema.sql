DROP TABLE IF EXISTS  customer;
DROP TABLE IF EXISTS  product;
DROP TABLE IF EXISTS  customer_order;

CREATE TABLE customer (
    id    INTEGER      PRIMARY KEY AUTOINCREMENT,
    name  TEXT (3, 16),
    user_name   TEXT (3, 8),
    password    TEXT (3, 8),
    email TEXT         UNIQUE
                       CONSTRAINT VALID_EMAIL CHECK (email LIKE '%_@__%.__%')
                       NOT NULL
);


CREATE TABLE product (
    id       INTEGER  PRIMARY KEY AUTOINCREMENT,
    name     TEXT (3, 50) NOT NULL,
    quantity NUMERIC  NOT NULL,
    price    NUMERIC  NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP
);

CREATE TABLE customer_order (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES product (id),
    customer_id INTEGER REFERENCES customer (id),
    quantity NUMERIC  NOT NULL,
    total_price  NUMERIC DEFAULT ,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);