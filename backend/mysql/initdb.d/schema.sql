CREATE TABLE users (
    id VARCHAR(32) NOT NULL,
    img MEDIUMBLOB NOT NULL,
    img_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (id)
)

CREATE TABLE products (
    id INTEGER,
    rounded_square_icon MEDIUMBLOB NOT NULL,
    circle_icon MEDIUMBLOB NOT NULL,
    PRIMARY KEY (id)
)
