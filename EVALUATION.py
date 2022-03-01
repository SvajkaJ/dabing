#!/usr/bin/python3
# Autor: SvajkaJ
# Date:  21.2.2022


from datetime import datetime # https://docs.python.org/3/library/datetime.html#module-datetime
from time import sleep
from dabing import sendTrap
from dabing import PostgresInterface
from dabing import getConfig, getAlarmConfig
import signal


class Evaluator:
    def __init__(self):
        self.snrState    = { "isOk": True, "tstz": 0, "trigger": 0 }
        self.berState    = { "isOk": True, "tstz": 0, "trigger": 0 }
        self.powerState  = { "isOk": True, "tstz": 0, "trigger": 0 }
        self.fiberState  = { "isOk": True, "tstz": 0, "trigger": 0 }
        self.signalState = { "isOk": True, "tstz": 0, "trigger": 0 }
        self.syncState   = { "isOk": True, "tstz": 0, "trigger": 0 }

    def updateConfig(self):
        self.config = getAlarmConfig()
        # config: { 'enabled': True, 'low': 20, 'high': 50, 'trigger': 10, 'min': 0, 'max': 80 }

    def __evaluateV(self, v, c, s, tstz: datetime):
        # if you pass a dictionary or a list to a function they are passed by reference
        if (c["enabled"] == False): # treat as everything is ok
            err = False
        elif (c["low"] > v):   # if sync (True) then low must be True
            err = True
        elif (c["high"] < v):  # copy low (True)
            err = True
        else:
            err = False

        if (err):
            if (s["isOk"]):
                s["isOk"] = False
                s["tstz"] = tstz.timestamp()
                s["trigger"] = c["trigger"]
        else:
            s["isOk"] = True
            s["tstz"] = 0
            s["trigger"] = 0

    def __evaluateS(self, s: dict, tstz: datetime):
        """False - ok \n\n True - error"""
        if (s["isOk"] == False):
            if (s["tstz"] + s["trigger"] > tstz.timestamp()):
                return False
            else:
                s["isOk"] = True
                s["tstz"] = 0
                s["trigger"] = 0
                return True
        else:
            return False

    def evaluateSNR(self, snr: float, tstz: datetime):
        self.__evaluateV(snr, self.config["snr"], self.snrState, tstz)
        return self.__evaluateS(self.snrState, tstz)

    def evaluateBER(self, ber: float, tstz: datetime):
        self.__evaluateV(ber, self.config["ber"], self.berState, tstz)
        return self.__evaluateS(self.berState, tstz)

    def evaluatePower(self, power: float, tstz: datetime):
        self.__evaluateV(power, self.config["power"], self.powerState, tstz)
        return self.__evaluateS(self.powerState, tstz)

    def evaluateFIBER(self, fiber: float, tstz: datetime):
        self.__evaluateV(fiber, self.config["fiber"], self.fiberState, tstz)
        return self.__evaluateS(self.fiberState, tstz)

    def evaluateSignal(self, signal: bool, tstz: datetime):
        self.__evaluateV(signal, self.config["signal"], self.signalState, tstz)
        return self.__evaluateS(self.signalState, tstz)

    def evaluateSync(self, sync: bool, tstz: datetime):
        self.__evaluateV(sync, self.config["sync"], self.syncState, tstz)
        return self.__evaluateS(self.syncState, tstz)


def onError(src):

    config = getConfig()
    host = config['managerHostname']
    port = config['managerPort']

    print("Sending SNMP Trap!")
    print(f"Alarm from \"{src}\"!")
    sendTrap(host, port, f"Alarm from \"{src}\"!")
    print("Trap sent successfully!")


running = True
def mySignalHandler(signum, frame):
    global running
    running = False


if __name__ == "__main__":
    signal.signal(signal.SIGINT,  mySignalHandler)
    signal.signal(signal.SIGTERM, mySignalHandler)

    try:
        # Init
        db = PostgresInterface()
        e = Evaluator()
        last_tstz = 0

        # Main never-ending loop
        while running:

            # Update alarm configuration
            e.updateConfig()

            # Build query
            if (last_tstz == 0):
                q = "SELECT * FROM dabing WHERE id = (SELECT MAX(id) FROM dabing)"
            else:
                q = f"SELECT * FROM dabing WHERE tstz > to_timestamp({last_tstz})"

            # Get new data
            records = db.execureQuery(q)
            # returns empty list when not a single record satisfies query
            # and that is safe to iterate over

            # Iterate over records
            for record in records:
                # record[0] == id
                # record[1] == snr
                # record[2] == ber
                # record[3] == power
                # record[4] == fiber
                # record[5] == signal (bool datatype)
                # record[6] == sync   (bool datatype)
                # record[7] == tstz   (datetime datatype)
                print("id:"    , str(record[0]).ljust(1), end=' | ')
                print("snr:"   , str(record[1]).ljust(10), end='| ')
                print("ber:"   , str(record[2]).ljust(15), end='| ')
                print("power:" , str(record[3]).ljust(10), end='| ')
                print("fiber:" , str(record[4]).ljust(14), end='| ')
                print("signal:", str(record[5]), end=' | ')
                print("sync:"  , str(record[6]), end=' | ')
                print("tstz:"  , record[-1].strftime('%Y-%m-%d %H:%M:%S%z'))

                if (e.evaluateSNR(record[1], record[-1])):
                    onError("snr")
                if (e.evaluateBER(record[2], record[-1])):
                    onError("ber")
                if (e.evaluatePower(record[3], record[-1])):
                    onError("power")
                if (e.evaluateFIBER(record[4], record[-1])):
                    onError("fiber")
                if (e.evaluateSignal(record[5], record[-1])):
                    onError("signal")
                if (e.evaluateSync(record[6], record[-1])):
                    onError("sync")

                last_tstz = record[-1].timestamp()

            sleep(1)  # the duration of sleep does not depend on the welle
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Program interrupted by user.")
    finally:
        print("EVALUATION.py closes down!")
