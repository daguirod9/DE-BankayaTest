CREATE TABLE IF NOT EXISTS item (
   id       SERIAL PRIMARY KEY,
   name_description    VARCHAR(255) NOT NULL,
   price_usd           FLOAT        NOT NULL,
   created_date        TIMESTAMP    NOT NULL,
   updated_date        TIMESTAMP    DEFAULT NULL
);

COMMENT ON TABLE item IS 'Data about items registered on shop';
COMMENT ON COLUMN item.id IS 'Item unique identifier on DB';
COMMENT ON COLUMN item.name_description IS 'Item name';
COMMENT ON COLUMN item.price_usd        IS 'Item price. This value can be updated';
COMMENT ON COLUMN item.created_date     IS 'Item Registration date';
COMMENT ON COLUMN item.updated_date     IS 'Item price update date';
