docker-compose up -d --build
psql postgres -c "\i ./data/create.sql"
