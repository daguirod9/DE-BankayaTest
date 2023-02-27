CREATE TABLE IF NOT EXISTS customer_oltp (
    id_oltp           INT,
    first_name        VARCHAR(50),
    last_name         VARCHAR(50),
    curp              VARCHAR(18),
    rfc               VARCHAR(13),
    phone_number      INT,
    created_date_ts   TIMESTAMP,
    replication_date  DATE
);

ALTER TABLE customer_oltp
ADD COLUMN address_desc VARCHAR(255) DEFAULT NULL;