In order to create .py module from .MIB file in ASN.1 notation use **mibdump.py**.
Following command worked for me:
```
mibdump.py --mib-source . --mib-source ../ --destination-directory ../ DABING-MIB
```
**do not forget** to change name of .MIB file at the very end of the commnad!
