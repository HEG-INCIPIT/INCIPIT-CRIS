#!/usr/bin/env bash

OS="`uname`"

if [ "$OS" == "Darwin" ]
then

    exit_script() {
        kill `ps -ef | grep 'java.*fuseki' | grep -v grep | awk '{ print $2 }'`
        kill $FIND_PID
    }

    trap exit_script SIGTERM SIGINT

    cd fuseki/
    ./fuseki-server &

    cd ..

    if [ -d "env/" ]; then
        . env/bin/activate
    else
        virtualenv -p python3 env
        pip install -r requirements.txt
    fi
elif [ "$OS" == "Linux" ]
then
    exit_script() {
        kill `ps -ef | grep 'java.*fuseki' | grep -v grep | awk '{ print $2 }'`
        kill $FIND_PID
    }
    kill $(pgrep java)
    trap exit_script SIGTERM SIGINT


    cd fuseki
    ./fuseki-server &

    cd ..

    if [ -d "env/" ]; then
        source env/bin/activate
    else
        virtualenv -p python3 env
        pip install -r requirements.txt
    fi

#elif [ "$OS" == "WindowsNT" ]
fi

python3 INCIPIT_CRIS/manage.py runserver 0.0.0.0:8000