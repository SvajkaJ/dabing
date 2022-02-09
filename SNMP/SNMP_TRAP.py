#!/usr/bin/python3

"""
Simple example of sending a notification (trap).
"""

from pysnmp.hlapi import *
from pysnmp.smi import builder, view
from os import getcwd
from uptime import *

HOST = '192.168.178.35'
PORT = 16200
VALUE = '100.0'

# Output:
# SNMPv2-MIB::sysUpTime.0
#     Object Name: 1.3.6.1.2.1.1.3.0
#     Value (Timeticks): 12345
# SNMPv2-MIB::snmpTrapOID.0
#     Object Name: 1.3.6.1.6.3.1.1.4.1.0
#     Value (OID): 1.3.6.1.6.3.1.1.5.7
# SNMPv2-MIB::snmpTrapEnterprise.0
#     Object Name: 1.3.6.1.6.3.1.1.4.3.0
#     Value (OID): 1.3.6.1.4.1.55532.3.1.1
# DABING-MIB::dabingPowerSpectralDensity.0
#     Object Name: 1.3.6.1.4.1.55532.3.2.1.0
#     Value (OctetString): "100.0"

# Assemble MIB view controller
mibBuilder = builder.MibBuilder()
mibBuilder.addMibSources(builder.DirMibSource(getcwd()))    # Adding path of my custom MIB
mibViewController = view.MibViewController(mibBuilder)

errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(
        SnmpEngine(),                                   # snmpEngine
        CommunityData('public'),                        # authData
        UdpTransportTarget((HOST, PORT)),               # transportTarget
        ContextData(),                                  # contextData
        'trap',                                         # notifyType
        # varBinds
        (
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0), uptime() * 100),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'snmpTrapOID', 0), '1.3.6.1.6.3.1.1.5.6'),
            ObjectType(
                ObjectIdentity('SNMPv2-MIB', 'snmpTrapEnterprise', 0),
                ObjectIdentity(
                    'DABING-MIB', 'dabingMalfunctioningBroadcastingTrap'
                ).resolveWithMib(mibViewController).getOid()
            ),
            ObjectType(
                ObjectIdentity('DABING-MIB', 'dabingPowerSpectralDensity', 0), OctetString(VALUE)
            ).addMibSource(
                getcwd()
            )
        )
    )
)

if errorIndication:
    print(errorIndication)
else:
    print("Trap sent successfully!")
