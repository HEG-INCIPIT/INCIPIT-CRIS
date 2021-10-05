# INCIPIT-CRIS

## INCIPIT-CRIS

INCIPIT-CRIS is a project developed at the HEG of Geneva. The purpose is to develop a Current Research Information System (CRIS) based on a triplestore and using ARKs to identify the different ressources that use ARKetype, a swiss option for creating Archival Resource Keys (ARKs).

Interaction scheme :

![alt text](INCIPIT-CRIS_Interactions.jpg "Logo Title Text 1")

## Fuseki

Fuseki is used as a standalone server. It is already configured to use one graph and an OWL reasoner.
User/Password are available in the file `fuseki/run/shiro.ini`.

## How tu run

Actually the shell script INCIPIT-CRIS_launcher.sh launch fuseki and django localhost on the port 8000.

Make sure to execute the script being in the folder, that it has the permissions to be run, and that the package `virtualenv` is already intalled (if you can install it using pip : `pip install virtualenv`). Then simply enter 

```bash
./INCIPIT-CRIS_launcher.sh
```

in the terminal.

If it's the first time that you run INCIPIT-CRIS you will need to add the schema.org ontology in the triplestore. To do so,
go in the folder `INCIPIT-CRIS` and run the following command :

```bash
python3 manage.py add_schema_to_cris
```

once you've done that, you're done and you can reach `localhost:8000` on your favourite navigator and enjoy !

