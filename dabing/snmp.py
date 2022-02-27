#!/usr/bin/python3


from pysnmp.hlapi import *
from pysnmp.smi import builder, view
from uptime import *
from dabing import getMIBSource


def sendTrap(host, port, payload):
    """
    Advanced example of sending a notification (trap).

    Sends 'dabingMalfunctioningBroadcastingTrap' with 'dabingGenericPayload' as a payload.
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
    # DABING-MIB::dabingGenericPayload.0
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
                        'DABING-MIB', 'dabingMalfunctioningBroadcastingTrap'
                    ).resolveWithMib(mibViewController).getOid()
                ),
                ObjectType(
                    ObjectIdentity('DABING-MIB', 'dabingGenericPayload', 0), OctetString(payload)
                ).addMibSource(myMIBSource)
            )
        )
    )

    if errorIndication:
        raise Exception("Unexpected error occured in sendTrap()!")


def testTrap(host, port, payload):
    """
    Advanced example of sending a notification (trap).

    Sends 'dabingTestTrap' with 'dabingGenericPayload' as a payload.
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
    # DABING-MIB::dabingGenericPayload.0
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
                        'DABING-MIB', 'dabingTestTrap'
                    ).resolveWithMib(mibViewController).getOid()
                ),
                ObjectType(
                    ObjectIdentity('DABING-MIB', 'dabingGenericPayload', 0), OctetString(payload)
                ).addMibSource(myMIBSource)
            )
        )
    )

    if errorIndication:
        raise Exception("Unexpected error occured in testTrap()!")


def simpleTrap(host, port, payload):
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


if __name__ == "__main__":

    host = "192.168.178.25"
    port = 162
    payload = f"Testing SNMP Trap."

    simpleTrap(host, port, payload)