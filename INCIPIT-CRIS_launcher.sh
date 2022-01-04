#!/usr/bin/env bash

############################################################
# Help                                                     #
############################################################
help()
{
    # Display Help
    echo "This script fully deploy and run the INCIPIT-CRIS, it is possible to only run some parts of the script."
    echo
    echo "Syntax: scriptTemplate [-a|d|f|h|s]"
    echo "options:"
    echo "a     Execute all the steps to deploy the CRIS"
    echo "d     Launch only Django"
    echo "f     Launch only Fuseki"
    echo "h     Print this Help"
    echo "m     Launch only Mysql"
    echo "s     Skip the mysql database verification"
    echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

mysql_f()
{
    echo "Checking mysql databases, you will be asked for the root password"

    if [ "`mysql -u root -p -e "SHOW DATABASES" | grep -w "incipit_cris"`" != "incipit_cris" ]
    then
        echo "Creating database and user with privelegies, you will be asked for the root password"
        mysql -u root -p -e "CREATE DATABASE incipit_cris; CREATE USER 'INCIPIT-CRIS'@'localhost' IDENTIFIED BY 'password'; GRANT ALL ON *.* TO 'INCIPIT-CRIS'@'localhost';"
    fi
}

fuseki()
{
    cd fuseki/
    ./fuseki-server &

    cd ..
}

django()
{
    if [ -d "env/" ]; then
        source env/bin/activate
    else
        virtualenv -p python3 env
        source env/bin/activate
        pip3 install -r requirements.txt
        python3 INCIPIT_CRIS/manage.py makemigrations INCIPIT_CRIS_app
        python3 INCIPIT_CRIS/manage.py migrate
        DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=pw DJANGO_SUPERUSER_EMAIL=admin@incipit-cris.com python3 INCIPIT_CRIS/manage.py createsuperuser --noinput
        python3 INCIPIT_CRIS/manage.py add_schema_to_cris
        python3 INCIPIT_CRIS/manage.py add_ark_to_admin
    fi

    python3 INCIPIT_CRIS/manage.py runserver 0.0.0.0:8000 &
}


test()
{
    source env/bin/activate
    cd INCIPIT_CRIS
    python3 manage.py test
}


kill_django(){
    if [ "`ps -ef | grep 'python' | grep -v grep | awk '{ print $2 }'`" ]
    then
        kill `ps -ef | grep 'python' | grep -v grep | awk '{ print $2 }'`
    fi
}


kill_fuseki(){
    if [ "`ps -ef | grep 'java.*fuseki' | grep -v grep | awk '{ print $2 }'`" ]
    then
        kill `ps -ef | grep 'java.*fuseki' | grep -v grep | awk '{ print $2 }'`
    fi
}


terminate() {

    case $flags in
        -d)
            kill_django
            ;;
        -f)
            kill_fuseki
            ;;
        -*)
            kill_django
            kill_fuseki
            ;;
    esac
    exit
}

trap terminate SIGTERM SIGINT

############################################################
# Process the input options.                               #
############################################################

flags=$1

export username_ark=""
export password_ark=""
export shoulder=""

while getopts "adfhmst" opt; do
    case $opt in
        a)
            mysql_f
            fuseki
            django
            ;;
        d)
            django
            ;;
        f)
            fuseki
            ;;
        h)
            help
            exit 0
            ;;
        m)
            mysql_f
            exit 0
            ;;
        s)
            fuseki
            django
            ;;
        t)
            test
            exit 0
            ;;
        \?) # unsupported flags
            echo "Error: Unsupported flag $1" >&2
            echo
            help
            exit 1
            ;;
    esac
done

if [ "$#" -gt "0" ]
then
    while :; do sleep 10000d; done
fi

help