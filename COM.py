import serial
import subprocess


p = subprocess.check_output("python -m serial.tools.list_ports")
ports = p.replace("\n", " ").split()
for i in range(len(ports)):
    print("port " + str(i) + " : " + ports[i])

port_n = input('Input port number: ')
print("Your select : " + str(ports[int(port_n)]))
port = ports[int(port_n)]

ser = serial.Serial(
    port = port,
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

def lth():
    try:
        ser.isOpen()
    except:
        return (0)
    try:
        ser.write("l")
    except:
        return (1)
    ser.close()
    return (2)
def lto():
    try:
        ser.isOpen()
    except:
        return (0)
    try:
        ser.write("lo")
    except:
        return (1)
    ser.close()
    return (2)

while ser.inWaiting() == 0:
    pass
#необходимая работа с данными...