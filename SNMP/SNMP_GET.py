#!/usr/bin/python3

"""
Simple example of SNMP GET request.
"""

from pysnmp.hlapi import *
from os import getcwd

HOST = '192.168.178.35'
PORT = 16100
OBJECT = 'dabingChannel'
#OBJECT = 'dabingDeviceHostname'
#OBJECT = 'dabingDeviceLocation'
#OBJECT = 'dabingDeviceStatus'

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget((HOST, PORT)),
        ContextData(),
        ObjectType(
            ObjectIdentity(
                'DABING-MIB', OBJECT, 0
            ).addMibSource(
                getcwd()
            )
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
