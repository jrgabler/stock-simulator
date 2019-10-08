CREATE TABLE IF NOT EXISTS myschema.User(
    id INT PRIMARY,
    username VARCHAR(15) NOT NULL UNIQUE,
)

CREATE TABLE IF NOT EXISTS myschema.LoginData(
    id INT PRIMARY,
    user_id INT NOT NULL REFERENCES User(id),
    password VARCHAR(20) NOT NULL /* TODO - this will require cryptographic functions on the application level */
)

CREATE TABLE IF NOT EXISTS myschema.Stock(
    id INT PRIMARY,
    open NUMERIC,
    close NUMERIC,
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
)

CREATE TABLE IF NOT EXISTS myschema.WatchList(
    id INT PRIMARY,
    stock_id INT NOT NULL REFERENCES Stock(id),
    user_id INT NOT NULL REFERENCES User(id)
)

CREATE TABLE IF NOT EXISTS myschema.SoldAssetsList(
    id INT PRIMARY,
    stock_id INT NOT NULL REFERENCES Stock(id),
    user_id INT NOT NULL REFERENCES User(id),
    quantity INT,
    date_purchased TIMESTAMP,
    date_sold TIMESTAMP,
    purchase_price NUMERIC NOT NULL,
    sale_price NUMERIC NOT NULL,
    position NUMERIC NOT NULL,
)

CREATE TABLE IF NOT EXISTS myschema.OwnedAssetsList(
    id INT PRIMARY,
    stock_id INT NOT NULL REFERENCES Stock(id),
    user_id INT NOT NULL REFERENCES USER(id),
    quantity INT,
    purchase_price NUMERIC NOT NULL,
    date_purchased TIMESTAMP NOT NULL,
    total_equity LONG NOT NULL,
)

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
