#!/bin/sh
echo "Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."
# Loop until mysqladmin can ping the database
until mysqladmin ping -h "$MYSQL_HOST" -P "$MYSQL_PORT" --silent; do
  sleep 2
done
echo "MySQL is ready!"
# Start the main command (Django)
exec "$@"

