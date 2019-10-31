DROP DATABASE IF EXISTS stocksimulator;
CREATE DATABASE stocksimulator;
\connect stocksimulator;

DROP TABLE IF EXISTS UserTable;
CREATE TABLE UserTable(
    id INT PRIMARY KEY,
    username VARCHAR(15) NOT NULL UNIQUE
);

DROP TABLE IF EXISTS LoginData;
CREATE TABLE LoginData(
    id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES UserTable(id),
    password VARCHAR(20) NOT NULL
);

DROP TABLE IF EXISTS Stock;
CREATE TABLE Stock(
    id INT PRIMARY KEY,
    open_price NUMERIC,
    close_price NUMERIC,
    high NUMERIC,
    low NUMERIC,
    average_volume REAL,
    market_cap REAL,
    peratio NUMERIC,
    dividend_yield NUMERIC,
    asset_type VARCHAR(10),
    last NUMERIC NOT NULL,
    symbol VARCHAR(8) NOT NULL,
    prev_close NUMERIC
);

DROP TABLE IF EXISTS WatchList;
CREATE TABLE WatchList(
    id INT PRIMARY KEY,
    stock_id INT NOT NULL REFERENCES Stock(id),
    user_id INT NOT NULL REFERENCES UserTable(id)
);

DROP TABLE IF EXISTS SoldAssetsList;
CREATE TABLE SoldAssetsList(
    id INT PRIMARY KEY,
    stock_id INT NOT NULL REFERENCES Stock(id),
    user_id INT NOT NULL REFERENCES UserTable(id),
    quantity INT,
    date_purchased TIMESTAMP,
    date_sold TIMESTAMP,
    purchase_price NUMERIC NOT NULL,
    sale_price NUMERIC NOT NULL,
    position NUMERIC NOT NULL
);

DROP TABLE IF EXISTS OwnedAssetsList;
CREATE TABLE OwnedAssetsList(
    id INT PRIMARY KEY,
    stock_id INT NOT NULL REFERENCES Stock(id),
    user_id INT NOT NULL REFERENCES UserTable(id),
    quantity INT,
    purchase_price NUMERIC NOT NULL,
    date_purchased TIMESTAMP NOT NULL,
    total_equity NUMERIC NOT NULL
);

CREATE OR REPLACE FUNCTION computed_position() 
    RETURNS trigger AS $BODY$
    BEGIN
        NEW.position = NEW.sale_price - NEW.purchase_price;
        RETURN NEW;
    END
    $BODY$ LANGUAGE plpgsql;

CREATE TRIGGER position_trigger
    BEFORE INSERT OR UPDATE
    ON SoldAssetsList
    FOR EACH ROW
        EXECUTE PROCEDURE computed_position();

CREATE OR REPLACE FUNCTION computed_equity()
    RETURNS trigger AS $BODY$
    BEGIN
        NEW.total_equity = NEW.quantity * NEW.purchase_price;
        RETURN NEW;
    END
    $BODY$ LANGUAGE plpgsql;

CREATE TRIGGER equity_trigger
    BEFORE INSERT OR UPDATE
    ON OwnedAssetsList
    FOR EACH ROW
        EXECUTE PROCEDURE computed_equity();
