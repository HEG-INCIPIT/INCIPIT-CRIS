#!/usr/bin/env bash

echo "START"
service mysql start
if [ "`mysql -e "SHOW DATABASES" | grep -w "incipit_cris"`" != "incipit_cris" ]
then
    echo
    echo OKAY
    echo
    mysql -e "CREATE DATABASE incipit_cris;"
    mysql -e "CREATE USER 'INCIPIT-CRIS'@'localhost' IDENTIFIED BY 'password';"
    mysql -e "GRANT ALL ON *.* TO 'INCIPIT-CRIS'@'localhost';"
fi

echo "RUN FUSEKI"

cd fuseki
./fuseki-server & >> fuseki.log

cd ..

echo "PYTHON"

if [ -d "env/" ]; then
    echo "ACTIVATE ENV"
    source env/bin/activate
else
    echo "VIRTUAL ENV"
    virtualenv -p python3.7 env
    echo "ACTIVATE ENV"
    source env/bin/activate
    echo "REQUIREMENTS"
    pip3 install -r requirements.txt
    echo "SETUP DJANGO ENVIRONEMENT"
    python3.7 INCIPIT_CRIS/manage.py migrate
    if [ `mysql -e "SHOW DATABASES" | grep -w "incipit_cris"` != "incipit_cris" ]
    then
        DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=pw DJANGO_SUPERUSER_EMAIL=admin@incipit-cris.com python3.7 INCIPIT_CRIS/manage.py createsuperuser --noinput
    fi
    echo "INSERTING SCHEMA.ORG ONTOLOGY INTO CRIS"
    python3.7 INCIPIT_CRIS/manage.py add_schema_to_cris
fi
echo "RUN SERVER"
python3.7 INCIPIT_CRIS/manage.py runserver 0.0.0.0:8000 --noreload