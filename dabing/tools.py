# Autor: SvajkaJ
# Datum: 22.3.2020

DABchannels = {
    # Band III
    174928000:  "5A",176640000:  "5B",178352000:  "5C",180064000:  "5D",
    181936000:  "6A",183648000:  "6B",185360000:  "6C",187072000:  "6D",
    188928000:  "7A",190640000:  "7B",192352000:  "7C",194064000:  "7D",
    195936000:  "8A",197648000:  "8B",199360000:  "8C",201072000:  "8D",
    202928000:  "9A",204640000:  "9B",206352000:  "9C",208064000:  "9D",
    209936000: "10A",211648000: "10B",213360000: "10C",215072000: "10D",
    216928000: "11A",218640000: "11B",220352000: "11C",222064000: "11D",
    223936000: "12A",225648000: "12B",227360000: "12C",229072000: "12D",
    230784000: "13A",232496000: "13B",234208000: "13C",235776000: "13D",237488000: "13E",239200000: "13F",

    # Band L
    # T-DAB
    1452960000: "LA",1454672000: "LB",1456384000: "LC",1458096000: "LD",
    1459808000: "LE",1461520000: "LF",1463232000: "LG",1464944000: "LH",
    1466656000: "LI",1468368000: "LJ",1470080000: "LK",1471792000: "LL",
    1473504000: "LM",1475216000: "LN",1476928000: "LO",1478640000: "LP",

    # S-DAB
    1480352000: "LQ",1482064000: "LR",1483776000: "LS",1485488000: "LT",
    1487200000: "LU",1488912000: "LV",1490624000: "LW",
}

def rFile(path):
    """Reads from a file."""
    try:
        with open(path, 'r') as f:    
            content = f.read()
        return content
    except:
        print("Error: Could not read from a file.")
        return False

def wFile(path, content=None):
    """Writes to a file."""
    try:
        with open(path, 'w') as f:    
            if content == None:
                return f
            else:
                content = str(content)
                if content[-1] == "\n":
                    f.write(content)
                else:
                    f.write(content + "\n")
                return True
    except:
        print("Error: Could not write to a file.")
        return False
