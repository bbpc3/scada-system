sensornames = [
    (b'Einschaltdauer', 'str'), 
    (b'T-Vorlauf', 'float'),
    (b'T-Heissgas', 'float'),
    (b'T-Aussen', 'float'),
    (b'T-Raum', 'float'),
    (b'T-Puffer', 'float'),
    (b'T-Boiler', 'float'),
    (b'T-Sauggas', 'float'),
    (b'T-WP2', 'float'),
    (b'T-Abtauung', 'float'),
    (b'T-Mischer', 'float'),
    (b'T-Raumsoll', 'float'),
    (b'T-Ruecklauf', 'float'),
    (b'Durchfluss', 'float'),
    (b'Pt1000 EVI', 'float'),
    (b'Steps EVI', 'float'),
    (b'Ueberhitz', 'float'),
    (b'Steps EEV', 'float'),
    (b'T-Verdampf', 'float'),
    (b'P-Sauggas', 'float'),
    (b'Solldrehz', 'float'),
    (b'MischPos', 'float'),
    (b'Mischer1', 'str')
]

startSymbol = b'\x0c\r\n'
endSymbol = b'\r\n\r\n'

def decode(data):
    values = {}

    startindex = data.find(startSymbol)
    data = data[startindex + len(startSymbol):]

    endIndex = data.find(endSymbol)
    data = data[:endIndex]
    data = data.replace(b"\xb0C", b"").replace(b"%", b"").replace(b"l/min", b"").replace(b"bar", b"").replace(b"T-R\xfccklauf", b"T-Ruecklauf")
    for (name, valuetype) in sensornames:
        try:
            if valuetype == "float":
                section = data[data.find(name) + len(name):]
                section = section[:section.find(b'\r\n')].decode("utf-8").replace(" ", "")
                values[name.decode("utf-8")] = float(section)
            else:
                section = data[data.find(name) + len(name):]
                section = section[:section.find(b'\r\n')].decode("utf-8").replace(":", "")
                values[name.decode("utf-8")] = section
        except:
            pass
    return values