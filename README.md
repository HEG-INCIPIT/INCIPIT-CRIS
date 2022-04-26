# INCIPIT-CRIS

## About INCIPIT-CRIS

INCIPIT-CRIS is a project developed at the HEG of Geneva. The purpose is to develop a Current Research Information System (CRIS) based on a triplestore and using ARKs to identify the different ressources that use ARKetype, a swiss option for creating Archival Resource Keys (ARKs).

Interaction scheme :

![alt text](INCIPIT-CRIS_Interactions.jpg "Logo Title Text 1")

## Fuseki

Fuseki is used as a standalone server. It is already configured to use one graph and an OWL reasoner.
User/Password are available in the file `fuseki/run/shiro.ini`.

## How to deploy

The easiest way to deploy INCIPIT-CRIS is to only download the file `docker-compose.yml`, and run it in docker with the command :

```bash
docker-compose up
```

It will automatically download the last docker image and run an instance of INCIPIT-CRIS on `localhost` and `localhost:8000`. 
Make sure that the ports `8000`, `80` and `443` are free.
With this configuration, as localhost has no certificates, it will notify it was unable to generate a certificate for the domain localhost.
However it will not entrave with the proper functioning of the CRIS.

If you want it to run on an defined URL you can edit the `docker-compose.yml` as indicated in the comments of the file.

## For development purposes

If you want to edit INCIPIT-CRIS to, for example, add a features that is not implemented, you can use the file `INCIPIT-CRIS_launcher.sh` that allows you to run localy and in an virtual environment the project.

First of all, make sure to have installed in the machine that will launch the script the following elements :

- `sudo apt install mysql-server`
- `sudo apt-get install libmysqlclient-dev`
- `sudo apt-get install python3`
- `sudo apt install python3-virtualenv`

Pay attention to the default policy level of the passwords in mysql. By default, the script will create an user which password is considered low by mysql. You can change it directly in the script.
Another element is the authentication plugin use by the root user. The script needs the plugin to be set as `mysql_native_password` to be able to connect to mysql.

If you fulfill all the prerequirements, then you can launch :

```bash
./INCIPIT-CRIS_launcher.sh 
```

Make sure to run it in its repertory **and** that the file has the rights to be executed, if not you can give it the rights using the `chmod` command :

```bash
chmod +x INCIPIT-CRIS_launcher.sh
```

## ARK minting

If you want to use the CRIS at it's fully potential, you'll need to use the ARK minter. For that, you should set the values for the variables : `username_ark`, `password_ark` and `shoulder` with yours in the docker-compose.yml or INCIPIT-CRIS_launcher.sh file, depending on which you use. (If you don't have any access yet you can contact www.arketype.ch)

## INCIPIT-CRIS_launcher.sh usage

- `a` : Execute all the steps to deploy the CRIS
- `d` : Launch only Django
- `f` : Launch only Fuseki
- `h` : Print this Help
- `m` : Launch only Mysql
- `s` : Skip the mysql database verification

You can combine flags.

## Populate Triplestore

### N-Triples

You can use N-Triples formats : `(ttl, n3, nt, rdf, owl, nq, trig, jsonld)` to populate the Triplestore. First of all, you'll need to upload the file to the `CRIS` by going to "Importer des données". After selecting the file, click on "importer". Then you can go to "Gérer les données", after clicking on "Triple file", you can see all the files that are N-Triples that you have upload. You can use them to populate the Triplestore. Delete them, or download them (one by one).

### CSV
It is possible to use CSV files instead of N-Triples to populate the Triplestore. To do so, you can first upload the file to the `CRIS` by going to "Importer des données". After selecting the file, click on "importer". Then you can go to "Gérer les données", after clicking on "CSV file", you can see all the CSV that were upload to the CRIS and perform some actions (populate, delete, download).

If you're using CSV, you should pay attention to the headers of the differents categories. You will found an example of all the headers and a line of data example in the folder `file_examples` -> `csv`. If you use a header that is not recognize, an error will be raised. The header is not case-sensitive and doesn't take care of the order of the data. If you don't have an ARK for a data, you can let the cell empty, the CRIS will automatically mint one.

:warning: **The delimiter used for the csv files are tabulations.**

In case you have more than one ark for a category, you can include them all within the delimiter separeted by one space.

For `Articles, Projects, Dataset, Institutions`, if you populate data with two times the same ARK, the first data will be override by the second one.

For `Person`, if there already exist one person with a duplicate ARK. It will only inform you at the end that the person with the given ARK could not be created.