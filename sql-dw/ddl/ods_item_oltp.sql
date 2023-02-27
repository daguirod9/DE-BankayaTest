CREATE TABLE IF NOT EXISTS item_oltp (
   id_oltp             INT,
   name_description    VARCHAR(255),
   price_usd           FLOAT,
   created_date        TIMESTAMP,
   updated_date        TIMESTAMP,
   replication_date    DATE
);