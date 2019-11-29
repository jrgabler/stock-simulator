docker-compose up -d --build
mysql -u user -p < "./data/create.sql"
