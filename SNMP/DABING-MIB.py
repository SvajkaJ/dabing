#
# PySNMP MIB module DABING-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://..\DABING-MIB.mib
# Produced by pysmi-0.3.4 at Fri Dec 25 21:14:58 2020
# On host ? platform ? version ? by user ?
# Using Python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 22:45:29) [MSC v.1916 32 bit (Intel)]
#
OctetString, ObjectIdentifier, Integer = mibBuilder.importSymbols("ASN1", "OctetString", "ObjectIdentifier", "Integer")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsIntersection, ConstraintsUnion, ValueSizeConstraint, SingleValueConstraint, ValueRangeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "ValueSizeConstraint", "SingleValueConstraint", "ValueRangeConstraint")
ModuleCompliance, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
Bits, Counter32, NotificationType, iso, MibIdentifier, Unsigned32, enterprises, ObjectIdentity, IpAddress, Gauge32, ModuleIdentity, Integer32, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64 = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Counter32", "NotificationType", "iso", "MibIdentifier", "Unsigned32", "enterprises", "ObjectIdentity", "IpAddress", "Gauge32", "ModuleIdentity", "Integer32", "TimeTicks", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Counter64")
DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
dabing = ModuleIdentity((1, 3, 6, 1, 4, 1, 55532))
dabing.setRevisions(('2020-10-21 00:00',))
if mibBuilder.loadTexts: dabing.setLastUpdated('202010210000Z')
if mibBuilder.loadTexts: dabing.setOrganization('www.stuba.sk')
dabingParameters = MibIdentifier((1, 3, 6, 1, 4, 1, 55532, 1))
dabingDeviceInfo = MibIdentifier((1, 3, 6, 1, 4, 1, 55532, 2))
dabingNotifications = MibIdentifier((1, 3, 6, 1, 4, 1, 55532, 3))
dabingNotificationPrefix = MibIdentifier((1, 3, 6, 1, 4, 1, 55532, 3, 1))
dabingNotificationObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 55532, 3, 2))
dabingChannel = MibScalar((1, 3, 6, 1, 4, 1, 55532, 1, 1), OctetString().clone('12C')).setMaxAccess("readwrite")
if mibBuilder.loadTexts: dabingChannel.setStatus('current')
dabingDeviceHostname = MibScalar((1, 3, 6, 1, 4, 1, 55532, 2, 1), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dabingDeviceHostname.setStatus('current')
dabingDeviceLocation = MibScalar((1, 3, 6, 1, 4, 1, 55532, 2, 2), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dabingDeviceLocation.setStatus('current')
dabingDeviceStatus = MibScalar((1, 3, 6, 1, 4, 1, 55532, 2, 3), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dabingDeviceStatus.setStatus('current')
dabingPowerSpectralDensity = MibScalar((1, 3, 6, 1, 4, 1, 55532, 3, 2, 1), OctetString().clone('0.0')).setMaxAccess("accessiblefornotify")
if mibBuilder.loadTexts: dabingPowerSpectralDensity.setStatus('current')
dabingMalfunctioningBroadcastingTrap = NotificationType((1, 3, 6, 1, 4, 1, 55532, 3, 1, 1)).setObjects(("DABING-MIB", "dabingPowerSpectralDensity"))
if mibBuilder.loadTexts: dabingMalfunctioningBroadcastingTrap.setStatus('current')
mibBuilder.exportSymbols("DABING-MIB", dabingDeviceInfo=dabingDeviceInfo, dabingParameters=dabingParameters, dabing=dabing, dabingNotifications=dabingNotifications, dabingDeviceStatus=dabingDeviceStatus, dabingDeviceLocation=dabingDeviceLocation, dabingNotificationObjects=dabingNotificationObjects, dabingDeviceHostname=dabingDeviceHostname, dabingPowerSpectralDensity=dabingPowerSpectralDensity, dabingMalfunctioningBroadcastingTrap=dabingMalfunctioningBroadcastingTrap, dabingChannel=dabingChannel, PYSNMP_MODULE_ID=dabing, dabingNotificationPrefix=dabingNotificationPrefix)
