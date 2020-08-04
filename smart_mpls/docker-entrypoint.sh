#!/bin/sh

cd $APP_PATH

# create tables
echo "Updating Database Tables"
./manage.py makemigrations
./manage.py migrate
echo "The Database has been updated"


# run the server
echo "Starting the server..."
python manage.py runserver