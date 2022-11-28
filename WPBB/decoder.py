marker1 = '\f\r\n'
marker2 = '\r\n\r\n'

def fixencoding(input):
    output = input.replace(b'\xb0', b"\xc2\xb0")
    output = output.replace(b'\xfc', b'\xc3\xbc')
    return output

def getSection(data : bytes) -> str:
    data = fixencoding(data)
    data = data.decode()
    #print(data[start:end])
    return data
    

def decode(match : str):
    values = {}
    for i in range(1, 10):
        values[f'E0{i}'] = "-"
        values[f'A0{i}'] = "-"
    for i in range(10, 17):
        if i < 12:
            values[f'E{i}'] = "-"
        values[f'A{i}'] = "-"
    lines = [x.strip() for x in match.splitlines()]
    split = [list(filter(None, x.split(" "))) for x in lines if len(x.split(" ")) > 1]
    for element in split:
        try:
            if len(element) == 3:
                try:
                    values[f'{element[0]} ({element[2]})'] = float(element[1])
                    continue
                except:
                    pass
                
            values[f'{element[0]}'] = " ".join(element[1:])
        except:
            pass
    for i in range(1, 10):
        if values[f'E0{i}'] == "-":
            values[f'E0{i}'] = 0
        else:
            values[f'E0{i}'] = 1
        if values[f'A0{i}'] == "-":
            values[f'A0{i}'] = 0
        else:
            values[f'A0{i}'] = 1
    for i in range(10, 17):
        if i < 12:
            if values[f'E{i}'] == "-":
                values[f'E{i}'] = 0
            else:
                values[f'E{i}'] = 1
        if values[f'A{i}'] == "-":
            values[f'A{i}'] = 0
        else:
            values[f'A{i}'] = 1
    return values