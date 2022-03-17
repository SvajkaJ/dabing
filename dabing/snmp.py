#!/usr/bin/python3
# Autor: SvajkaJ
# Datum: 28.2.2022

from pysnmp.hlapi import *
from pysnmp.smi import builder, view
from uptime import *

try:
    from .tools import getMIBSource
except:
    from tools import getMIBSource


def sendTrap(host, port, payload):
    """
    Advanced example of sending a notification (trap).

    Sends 'malfunctionTrap' with 'genericPayload' as a payload.
    Manager's hostname (IP address) and port must be passed as an argument to the function.
    Throws a generic Exception when error occurs.
    """

    myMIBSource = getMIBSource()

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
    # DABING-MIB::genericPayload.0
    #     Object Name: 1.3.6.1.4.1.55532.3.2.1.0
    #     Value (OctetString): "Value"

    # Assemble MIB view controller
    mibBuilder = builder.MibBuilder()
    mibBuilder.addMibSources(builder.DirMibSource(myMIBSource))    # Adding path of my custom MIB
    mibViewController = view.MibViewController(mibBuilder)

    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),                                   # snmpEngine
            CommunityData('public'),                        # authData
            UdpTransportTarget((host, port)),               # transportTarget
            ContextData(),                                  # contextData
            'trap',                                         # notifyType
            # varBinds
            (
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0), uptime() * 100),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'snmpTrapOID', 0), '1.3.6.1.6.3.1.1.5.6'),
                ObjectType(
                    ObjectIdentity('SNMPv2-MIB', 'snmpTrapEnterprise', 0),
                    ObjectIdentity(
                        'DABING-MIB', 'malfunctionTrap'
                    ).resolveWithMib(mibViewController).getOid()
                ),
                ObjectType(
                    ObjectIdentity('DABING-MIB', 'genericPayload', 0), OctetString(payload)
                ).addMibSource(myMIBSource)
            )
        )
    )

    if errorIndication:
        raise Exception("Unexpected error occured in sendTrap()!")


def testTrap(host, port, payload):
    """
    Advanced example of sending a notification (trap).

    Sends 'testTrap' with 'genericPayload' as a payload.
    Manager's hostname (IP address) and port must be passed as an argument to the function.
    Throws a generic Exception when error occurs.
    """

    myMIBSource = getMIBSource()

    # Output:
    # SNMPv2-MIB::sysUpTime.0
    #     Object Name: 1.3.6.1.2.1.1.3.0
    #     Value (Timeticks): 12345
    # SNMPv2-MIB::snmpTrapOID.0
    #     Object Name: 1.3.6.1.6.3.1.1.4.1.0
    #     Value (OID): 1.3.6.1.6.3.1.1.5.7
    # SNMPv2-MIB::snmpTrapEnterprise.0
    #     Object Name: 1.3.6.1.6.3.1.1.4.3.0
    #     Value (OID): 1.3.6.1.4.1.55532.3.1.2
    # DABING-MIB::genericPayload.0
    #     Object Name: 1.3.6.1.4.1.55532.3.2.1.0
    #     Value (OctetString): "Value"

    # Assemble MIB view controller
    mibBuilder = builder.MibBuilder()
    mibBuilder.addMibSources(builder.DirMibSource(myMIBSource))    # Adding path of my custom MIB
    mibViewController = view.MibViewController(mibBuilder)

    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),                                   # snmpEngine
            CommunityData('public'),                        # authData
            UdpTransportTarget((host, port)),               # transportTarget
            ContextData(),                                  # contextData
            'trap',                                         # notifyType
            # varBinds
            (
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0), uptime() * 100),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'snmpTrapOID', 0), '1.3.6.1.6.3.1.1.5.6'),
                ObjectType(
                    ObjectIdentity('SNMPv2-MIB', 'snmpTrapEnterprise', 0),
                    ObjectIdentity(
                        'DABING-MIB', 'testTrap'
                    ).resolveWithMib(mibViewController).getOid()
                ),
                ObjectType(
                    ObjectIdentity('DABING-MIB', 'genericPayload', 0), OctetString(payload)
                ).addMibSource(myMIBSource)
            )
        )
    )

    if errorIndication:
        raise Exception("Unexpected error occured in testTrap()!")


def __SNMP_TRAP(host, port, payload):
    """
    Simple example of sending a notification (trap).

    Manager's hostname (IP address) and port must be passed as an argument to the function.
    Throws a generic Exception when error occurs.
    """
    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget((host, port)),
            ContextData(),
            'trap',
            (
                ("1.3.6.1.2.1.1.1.0", OctetString(payload))
            )
            # .0 at the end of every variable signifies it is a scalar 
        )
    )

    if errorIndication:
        raise Exception("Unexpected error occured in simpleTrap()!")


def __SNMP_GET(host, port, obj):
    """Executes SNMP GET request of any object in DABING-MIB.MIB."""

    myMIBSource = getMIBSource()

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(
                ObjectIdentity(
                    'DABING-MIB', obj, 0
                ).addMibSource(myMIBSource)
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


def __SNMP_SET(host, port, obj, value):
    """Executes SNMP SET request of any object in DABING-MIB.MIB."""

    myMIBSource = getMIBSource()

    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(
                ObjectIdentity(
                    'DABING-MIB', obj, 0
                ).addMibSource(myMIBSource),
                value
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


if __name__ == "__main__":

    objs = [
        ('channel', '10A'),             # Type: OCTET STRING    read-only
        ('interval', 500),              # Type: Integer32       read-only
        ('trapEnabled', 1),             # Type: Integer32       read-write
        ('agentIdentifier', 1),         # Type: Integer32       read-write
        ('agentLabel', 'Test'),         # Type: OCTET STRING    read-write
        ('agentStatus', 0),             # Type: Integer32       read-only
        ('managerHostname', '0.0.0.0'), # Type: OCTET STRING    read-only
        ('managerPort', 162)            # Type: Integer32       read-only
    ]

    # Testing GET request
    for obj in objs:
        __SNMP_GET('192.168.178.35', 16100, obj[0])

    # Testing SET request
    for obj in objs:
        __SNMP_SET('192.168.178.35', 16100, obj[0], obj[1])

    # Testing Trap
    #__SNMP_TRAP('192.168.178.25', 162, f"Testing SNMP Trap.")
