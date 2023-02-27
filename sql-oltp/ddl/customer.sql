CREATE TABLE IF NOT EXISTS customer (
    id                SERIAL PRIMARY KEY,
    first_name        VARCHAR(50)   NOT NULL,
    last_name         VARCHAR(50)   NOT NULL,
    curp              VARCHAR(18)   UNIQUE NOT NULL,
    rfc               VARCHAR(13)   ,
    phone_number      INT,
    created_date_TS   TIMESTAMP     NOT NULL
);

COMMENT ON TABLE customer IS 'Data about Bankaya customers';
COMMENT ON COLUMN customer.id IS ' Bnakaya Customer unique identifier on DB. This values is taken from an autoincremental reference';
COMMENT ON COLUMN customer.first_name IS 'Bankaya customer first name';
COMMENT ON COLUMN customer.last_name IS 'Bankaya customer last name';
COMMENT ON COLUMN customer.curp IS 'Bankaya customer Mexico person unique key';
COMMENT ON COLUMN customer.rfc IS 'Bankaya customer Mexico fiscal entity unique key';
COMMENT ON COLUMN customer.phone_number IS 'Bankaya customer contact phone number';
COMMENT ON COLUMN customer.created_date_TS IS 'Bankaya customer registration timestamp';

ALTER TABLE customer 
ADD COLUMN address_desc VARCHAR(255) DEFAULT NULL;