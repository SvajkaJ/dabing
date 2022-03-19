## SNMP libraries for Python
**PySNMP**
https://github.com/etingof/pysnmp
https://pysnmp.readthedocs.io/en/latest/index.html

**Easy SNMP**
https://easysnmp.readthedocs.io/en/latest/


## Private Enterprise
You can't just create a custom OID yourself, you have to apply for one!

You can create any OID you want under your enterprise number. 
Outside of your enterprise branch, you cannot. If you want to 
create one under your enterprise number, you probably need to 
coordinate with the cognizant individual in your company who is 
responsible for managing that, but anything under your enterprise 
number remains totally under your company's purview.

**Private Enterprise Number (PEN) Request**
http://pen.iana.org/pen/PenApplication.page

I got:
```
55532
Katze Laboratories
Tom Katze
f*kater@gmail.com
```

**Custom MIB**
MIB is a text file described by ASN.1 language. To compile plain MIB into pysnmp form 
you should use the pysnmp/tools/build-pysnmp-mib script or mibdump.py. If you are running SNMP 
management application, you do not really need to compile MIBs explicitly -- pysnmp 
will do that for you behind the scenes by calling pysmi compiler and caching compiled 
MIB for future occasions.

In order to create .py module from .MIB file in ASN.1 notation use **mibdump.py** in *install/lib* directory.

Following command worked for me. Make sure you are in the *lib* directory when executing the command.
```
mibdump.py --mib-source . --mib-source ../ --destination-directory ../ DABING-MIB
```
