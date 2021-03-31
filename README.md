# INCIPIT-CRIS

## INCIPIT-CRIS

## Fuseki

We use Fuseki by adding a new folder in its files (`cd fuseki/` and then `mkir NAME`) that will be used to contain the dataset.
Then you can simply start fuseki by running `./fuseki-server --tdb2 --loc=NAME/ /INCIPIT-CRIS` and replace `NAME` by the
name of the folder for dataset.
User/Password are available in the file `fuseki/run/shiro.ini`.
