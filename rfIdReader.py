import serial

def rf_id_input():
    device = serial.Serial('/dev/ttyUSB0', 9600)
    code = ''
    while True:
        data = device.read()
        code += data
        if str(data) == '\r':
            break

    print('Raw data: ' + str(code))

    return format_input(code)

def format_input(raw_code):
    new_code = ''.join(e for e in raw_code if e.isalnum())
    print('Formatted data: ' + str(new_code))
    return new_code