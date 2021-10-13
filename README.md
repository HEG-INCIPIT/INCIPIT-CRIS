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

```bash
./INCIPIT-CRIS_launcher.sh 
```

Make sure to run it in its repertory **and** that the file has the rights to be executed, if not you can give it the rights using the `chmod` command :

```bash
chmod +x INCIPIT-CRIS_launcher.sh
```

### INCIPIT-CRIS_launcher.sh usage

- `a` : Execute all the steps to deploy the CRIS
- `d` : Launch only Django
- `f` : Launch only Fuseki
- `h` : Print this Help
- `m` : Launch only Mysql
- `s` : Skip the mysql database verification

You can combine flags.