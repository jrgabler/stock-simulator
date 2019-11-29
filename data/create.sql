DROP DATABASE IF EXISTS stocksimulator;
CREATE DATABASE stocksimulator;
use stocksimulator;

DROP TABLE IF EXISTS UserTable;
CREATE TABLE UserTable(
    id int NOT NULL AUTO_INCREMENT,
    username VARCHAR(15) NOT NULL UNIQUE,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS LoginData;
CREATE TABLE LoginData(
    id int NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    password VARCHAR(20) NOT NULL,
    salt VARCHAR(64) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN  KEY (user_id) REFERENCES UserTable(id)
);

DROP TABLE IF EXISTS RevokedTokens;
CREATE TABLE RevokedTokens(
    id int NOT NULL AUTO_INCREMENT,
    jti VARCHAR(120) NOT NULL,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS Stock;
CREATE TABLE Stock(
    id int NOT NULL AUTO_INCREMENT,
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
    prev_close NUMERIC,
    PRIMARY KEY (id),
    UNIQUE KEY symbol (symbol)
);

DROP TABLE IF EXISTS WatchList;
CREATE TABLE WatchList(
    id int NOT NULL AUTO_INCREMENT,
    stock_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN  KEY (stock_id) REFERENCES Stock(id),
	FOREIGN  KEY (user_id) REFERENCES UserTable(id)
);

DROP TABLE IF EXISTS SoldAssetsList;
CREATE TABLE SoldAssetsList(
    id int NOT NULL AUTO_INCREMENT,
    stock_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT,
    date_purchased TIMESTAMP,
    date_sold TIMESTAMP,
    purchase_price NUMERIC NOT NULL,
    sale_price NUMERIC NOT NULL,
    position NUMERIC NOT NULL,
    PRIMARY KEY(id),
    FOREIGN  KEY (stock_id) REFERENCES Stock(id),
	FOREIGN  KEY (user_id) REFERENCES UserTable(id)
);

DROP TABLE IF EXISTS OwnedAssetsList;
CREATE TABLE OwnedAssetsList(
    id int NOT NULL AUTO_INCREMENT,
    stock_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT,
    purchase_price NUMERIC NOT NULL,
    date_purchased TIMESTAMP NOT NULL,
    total_equity NUMERIC NOT NULL,
    PRIMARY KEY(id),
    FOREIGN  KEY (stock_id) REFERENCES Stock(id),
	FOREIGN  KEY (user_id) REFERENCES UserTable(id)
);

DROP PROCEDURE IF EXISTS computed_position;
DELIMITER //
CREATE PROCEDURE computed_position()
BEGIN
	SELECT (NEW.sale_price - NEW.purchase_price) as compPrice
	from SoldAssetsList;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS position_trigger;
DELIMITER //
CREATE TRIGGER position_trigger
    BEFORE UPDATE 
    ON SoldAssetsList
    FOR EACH ROW
    BEGIN
        CALL computed_position();
	END;//
DELIMITER ;

DROP PROCEDURE IF EXISTS computed_equity;
DELIMITER //
CREATE PROCEDURE computed_equity()
BEGIN
	SELECT (quantity * purchase_price) as total_equity
	from OwnedAssetsList;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS equity_trigger;
DELIMITER //
CREATE TRIGGER equity_trigger
    BEFORE UPDATE 
    ON OwnedAssetsList
    FOR EACH ROW
    BEGIN
        CALL computed_equity();
	END;//
DELIMITER ;