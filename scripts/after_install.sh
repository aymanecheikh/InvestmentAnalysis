#!/bin/bash
cd /var/www/investment-analysis

# Create and activate virtual environment
pipenv install
pipenv shell

# Install MySQL and Python MySQL adapter
sudo apt-get update
sudo apt-get install -y mysql-server python3-dev default-libmysqlclient-dev build-essential

# Create and activate virtual environment
pipenv install
pipenv shell
pipenv install mysqlclient

# Create database and user (securely using Parameter Store credentials)
DB_PASSWORD=$(aws ssm get-parameter --name "/investment_analysis/django/settings/secret_key" --with-decryption --query "Parameter.Value" --output text)

# Create database and user
sudo mysql -e "CREATE DATABASE investment_analysis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'aymane'@'localhost' IDENTIFIED BY '$DB_PASSWORD';"
sudo mysql -e "GRANT ALL PRIVILEGES ON investment_analysis.* TO 'aymane'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Run migrations and collect static files
python manage.py makemigrations
python manage.py migrate
