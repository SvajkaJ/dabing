#!/usr/bin/python3

"""
Advanced example of SNMP Server responding to SNMP GET/SET queries.
"""

from pysnmp.smi import builder
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context, ntfrcv
from pysnmp.carrier.asyncore.dgram import udp
import json
from os import getcwd

HOST = '192.168.178.24'
PORT = 16100
PORT_TRAP = 16200

# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# --------------------------- #
# ----- Transport Setup ----- #
# --------------------------- #

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode((HOST, PORT))
)

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName + (2,),
    udp.UdpTransport().openServerMode((HOST, PORT_TRAP))
)

# --------------------------- #
# ------ SNMPv2c Setup ------ #
# --------------------------- #

# SecurityName <-> CommunityName mapping.
config.addV1System(snmpEngine, 'my-area', 'public')

# Allow read MIB access for this user / securityModels at VACM
config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', (1, 3, 6))

# Create an SNMP context
snmpContext = context.SnmpContext(snmpEngine)

# ---------------------------------------------- #
# --- Create Custom Managed Object Instances --- #
# ---------------------------------------------- #

mibBuilder = snmpContext.getMibInstrum().getMibBuilder()
# Adding path of my custom MIB
mibBuilder.addMibSources(builder.DirMibSource(getcwd()))

# A base class for a custom Managed Object
MibScalarInstance, = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')


def getConfiguration():
    # Read current configuration
    with open('../config.json', 'r') as f:
        return json.loads(f.read())

def setConfiguration(key, value):
    data = getConfiguration()
    # Set new value
    data[key] = value
    # Save new configuration
    with open('../config.json', 'w') as f:
        f.write(str(json.dumps(data)))

class dabingChannelClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfiguration()["dabingChannel"]
        return name, self.syntax.clone(value)
    def writeCommit(self, name, val, idx, acInfo):
        setConfiguration("dabingChannel", str(val))

class dabingDeviceHostnameClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfiguration()["dabingDeviceHostname"]
        return name, self.syntax.clone(value)
    def writeCommit(self, name, val, idx, acInfo):
        setConfiguration("dabingDeviceHostname", str(val))

class dabingDeviceLocationClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfiguration()["dabingDeviceLocation"]
        return name, self.syntax.clone(value)
    def writeCommit(self, name, val, idx, acInfo):
        setConfiguration("dabingDeviceLocation", str(val))

class dabingDeviceStatusClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfiguration()["dabingDeviceLocation"]
        return name, self.syntax.clone(value)
    def writeCommit(self, name, val, idx, acInfo):
        setConfiguration("dabingDeviceStatus", int(val))

# --------------------------------------------- #
# --- Managed Object Instance Specification --- #
# --------------------------------------------- #

dabingChannel, dabingDeviceHostname, dabingDeviceLocation, dabingDeviceStatus, = mibBuilder.importSymbols(
    'DABING-MIB',
    'dabingChannel',
    'dabingDeviceHostname',
    'dabingDeviceLocation',
    'dabingDeviceStatus'
)

dabingChannelInstance = dabingChannelClassInstance(
    dabingChannel.name, (0,), dabingChannel.syntax
)

dabingDeviceHostnameInstance = dabingDeviceHostnameClassInstance(
    dabingDeviceHostname.name, (0,), dabingDeviceHostname.syntax
)

dabingDeviceLocationInstance = dabingDeviceLocationClassInstance(
    dabingDeviceLocation.name, (0,), dabingDeviceLocation.syntax
)

dabingDeviceStatusInstance = dabingDeviceStatusClassInstance(
    dabingDeviceStatus.name, (0,), dabingDeviceStatus.syntax
)

# Register Managed Object with a MIB tree
mibBuilder.exportSymbols(
    # '__' prefixed MIB modules take precedence on indexing
    '__MY-DABING-MIB',
    dabingChannelInstance = dabingChannelInstance,
    dabingDeviceHostnameInstance = dabingDeviceHostnameInstance,
    dabingDeviceLocationInstance = dabingDeviceLocationInstance,
    dabingDeviceStatusInstance = dabingDeviceStatusInstance
)

# ----------------------------------------------------- #
# --- End of Managed Object Instance Initialization --- #
# ----------------------------------------------------- #

# Callback function for receiving notifications
def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    print(
        'Received notification from ContextEngineId "%s", ContextName "%s"' 
        % (contextEngineId.prettyPrint(), contextName.prettyPrint())
    )
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

# Register an imaginary never-ending job to keep I/O dispatcher running forever
snmpEngine.transportDispatcher.jobStarted(1)

print("SNMP Server running at %s, ports: %s, %s !" % (HOST, PORT, PORT_TRAP))
# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()
except KeyboardInterrupt:
    print("Closing Server!")
finally:
    snmpEngine.transportDispatcher.closeDispatcher()
