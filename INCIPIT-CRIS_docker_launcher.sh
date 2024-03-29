#!/bin/sh

echo "START"
service mysql start
first_launch=false
if [ "`mysql -e "SHOW DATABASES" | grep -w "incipit_cris"`" != "incipit_cris" ]
then
    first_launch=true
    mysql -e "CREATE DATABASE incipit_cris;"
    mysql -e "CREATE USER 'INCIPIT-CRIS'@'localhost' IDENTIFIED BY 'password';"
    mysql -e "GRANT ALL ON *.* TO 'INCIPIT-CRIS'@'localhost';"
fi

echo "RUN FUSEKI"

cd fuseki
./fuseki-server & >> fuseki.log

cd ..

echo "PYTHON"

echo "REQUIREMENTS"
pip3 install -r requirements.txt
echo "SETUP DJANGO ENVIRONEMENT"
python3.7 INCIPIT_CRIS/manage.py makemigrations INCIPIT_CRIS_app
python3.7 INCIPIT_CRIS/manage.py migrate
if [ "$first_launch" = true ]
then
    DJANGO_SUPERUSER_USERNAME=$username DJANGO_SUPERUSER_PASSWORD=$password DJANGO_SUPERUSER_EMAIL=admin@incipit-cris.com python3.7 INCIPIT_CRIS/manage.py createsuperuser --noinput
    python3.7 INCIPIT_CRIS/manage.py add_ark_to_admin
fi
echo "INSERTING SCHEMA.ORG ONTOLOGY INTO CRIS"
python3.7 INCIPIT_CRIS/manage.py add_schema_to_cris

echo "RUN SERVER"
python3.7 INCIPIT_CRIS/manage.py runserver 0.0.0.0:8000 --noreload