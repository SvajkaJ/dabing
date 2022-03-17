#!/usr/bin/python3
# Autor: SvajkaJ
# Datum: 27.2.2022

"""
Advanced example of SNMP Server responding to SNMP GET/SET queries.
"""

from pysnmp.smi import builder
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context, ntfrcv
from pysnmp.carrier.asyncore.dgram import udp
import signal

from dabing import getConfig, updateConfig, getMIBSource, get_status

HOST = '0.0.0.0'
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
mibBuilder.addMibSources(builder.DirMibSource(getMIBSource()))

# A base class for a custom Managed Object
MibScalarInstance, = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')

# read-only
class channelClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfig()["band"]["channel"]
        return name, self.syntax.clone(value)

# read-only
class intervalClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfig()["interval"]
        return name, self.syntax.clone(int(value))

#read-write
class trapEnabledClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        if getConfig()["trapEnabled"]:
            value = 1
        else:
            value = 0
        return name, self.syntax.clone(value)
    def writeCommit(self, name, val, idx, acInfo):
        if (val == 0):
            updateConfig({ "trapEnabled": False })
        elif (val == 1):
            updateConfig({ "trapEnabled": True })

# read-write
class agentIdentifierClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfig()["agentIdentifier"]
        return name, self.syntax.clone(value)
    def writeCommit(self, name, val, idx, acInfo):
        updateConfig({ "agentIdentifier": int(val) })

# read-write
class agentLabelClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfig()["agentLabel"]
        return name, self.syntax.clone(value)
    def writeCommit(self, name, val, idx, acInfo):
        updateConfig({ "agentLabel": str(val) })

# read-only
class agentStatusClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        if get_status(getConfig()):
            value = 1
        else:
            value = 0
        return name, self.syntax.clone(value)

# read-only
class managerHostnameClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfig()["managerHostname"]
        return name, self.syntax.clone(value)

# read-only
class managerPortClassInstance(MibScalarInstance):
    def readGet(self, name, *args):
        print("Value %s has been requested!" % (str(name).replace(", ", ".")[1:-1]))
        value = getConfig()["managerPort"]
        return name, self.syntax.clone(value)

# --------------------------------------------- #
# --- Managed Object Instance Specification --- #
# --------------------------------------------- #

channel, interval, trapEnabled, agentIdentifier, agentLabel, agentStatus, managerHostname, managerPort, = mibBuilder.importSymbols(
    'DABING-MIB',
    'channel',
    'interval',
    'trapEnabled',
    'agentIdentifier',
    'agentLabel',
    'agentStatus',
    'managerHostname',
    'managerPort'
)

channelInstance = channelClassInstance(
    channel.name, (0,), channel.syntax
)

intervalInstance = intervalClassInstance(
    interval.name, (0,), interval.syntax
)

trapEnabledInstance = trapEnabledClassInstance(
    trapEnabled.name, (0,), trapEnabled.syntax
)

agentIdentifierInstance = agentIdentifierClassInstance(
    agentIdentifier.name, (0,), agentIdentifier.syntax
)

agentLabelInstance = agentLabelClassInstance(
    agentLabel.name, (0,), agentLabel.syntax
)

agentStatusInstance = agentStatusClassInstance(
    agentStatus.name, (0,), agentStatus.syntax
)

managerHostnameInstance = managerHostnameClassInstance(
    managerHostname.name, (0,), managerHostname.syntax
)

managerPortInstance = managerPortClassInstance(
    managerPort.name, (0,), managerPort.syntax
)

# Register Managed Object with a MIB tree
mibBuilder.exportSymbols(
    # '__' prefixed MIB modules take precedence on indexing
    '__MY-DABING-MIB',
    channelInstance = channelInstance,
    intervalInstance = intervalInstance,
    trapEnabledInstance = trapEnabledInstance,
    agentIdentifierInstance = agentIdentifierInstance,
    agentLabelInstance = agentLabelInstance,
    agentStatusInstance = agentStatusInstance,
    managerHostnameInstance = managerHostnameInstance,
    managerPortInstance = managerPortInstance
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

def mySignalHandler(signum, frame):
    global snmpEngine
    snmpEngine.transportDispatcher.jobFinished(1)

signal.signal(signal.SIGINT,  mySignalHandler)
signal.signal(signal.SIGTERM, mySignalHandler)

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
    print("SNMP_SERVER.py closes down!")
    snmpEngine.transportDispatcher.closeDispatcher()
