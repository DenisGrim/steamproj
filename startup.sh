#!/bin/bash
set -e

echo "Starting PostgreSQL..."
# Start PostgreSQL in the background
docker-entrypoint.sh postgres &
PG_PID=$!

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -U user; do
  sleep 2
done
echo "PostgreSQL is ready!"

# Run ETL
echo "Running ETL..."
cd /etl
python3 transformer.py
until test -f /mydata/setup-complete; do
  sleep 2
done
echo "ETL started!"

# Run scrape
echo "Running scrape..."
cd /scrape
python3 scrape_reviews.py
echo "Scrape complete!"


