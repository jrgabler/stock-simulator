docker-compose up -d --build
mysql -u root < "./data/create.sql"
