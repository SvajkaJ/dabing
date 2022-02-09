#!/usr/bin/python3

"""
Simple example of SNMP SET query.
"""

from pysnmp.hlapi import *
from os import getcwd

HOST = '192.168.178.24'
PORT = 16100

# ---
OBJECT = 'dabingChannel'
VALUE = '12C'                           # Type: OCTET STRING
# ---
#OBJECT = 'dabingDeviceHostname'
#VALUE = 'TestHostname'                  # Type: OCTET STRING
# ---
#OBJECT = 'dabingDeviceLocation'
#VALUE = 'TestLocation'                  # Type: OCTET STRING
# ---
#OBJECT = 'dabingDeviceStatus'
#VALUE = 1                               # Type: Integer32

errorIndication, errorStatus, errorIndex, varBinds = next(
    setCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget((HOST, PORT)),
        ContextData(),
        ObjectType(
            ObjectIdentity(
                'DABING-MIB', OBJECT, 0
            ).addMibSource(
                getcwd()
            ),
            VALUE
        )
    )
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
