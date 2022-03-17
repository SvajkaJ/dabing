In order to create .py module from .MIB file in ASN.1 notation use **mibdump.py**.

Following command worked for me. Make sure you are in the *lib* directory when executing the command.
```
mibdump.py --mib-source . --mib-source ../ --destination-directory ../ DABING-MIB
```
