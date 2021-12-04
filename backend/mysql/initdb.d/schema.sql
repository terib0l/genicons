CREATE TABLE user (
    user_id VARCHAR(32) NOT NULL,
    img MEDIUMBLOB NOT NULL,
    img_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (user_id)
)

CREATE TABLE product (
    id VARCHAR(32) NOT NULL,
    rounded_square_icon MEDIUMBLOB NOT NULL,
    circle_icon MEDIUMBLOB NOT NULL,
    PRIMARY KEY (id)
)
