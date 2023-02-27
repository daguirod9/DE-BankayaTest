CREATE TABLE IF NOT EXISTS item_bought (
    order_id            BIGINT NOT NULL,
    total_amount        FLOAT  NOT NULL,
    created_date_ts     TIMESTAMP NOT NULL,
    customer_id         INT     NOT NULL,
    item_id             INT     NOT NULL,
    comments_desc       VARCHAR(255),
    FOREIGN KEY (customer_id)
      REFERENCES customer (id),
    FOREIGN KEY (item_id)
      REFERENCES item (id)
);