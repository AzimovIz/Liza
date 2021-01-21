import serial

ser = serial.Serial(
    port = 'COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None)

def htr():
    try:
        ser.isOpen()
    except:
        return(0)
    try:
        ser.write("h")
    except:
        return(1)
    ser.close()
    return(2)

def com2():
    pass

def com3():
    pass

while ser.inWaiting() == 0:
    pass
#необходимая работа с данными...