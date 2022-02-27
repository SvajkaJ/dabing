In order to create .py module from .MIB file in ASN.1 notation use **mibdump.py**.
Following command worked for me:
```
mibdump.py --mib-source . --mib-source ../ --destination-directory ../ DABING-MIB
```
It is assumed that the file ends with .MIB at the very end (of the commnad)!
