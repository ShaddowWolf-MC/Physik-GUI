import serial
import time
comport = 'Com5'
baudrate = 115200
arduinoData = serial.Serial(comport, baudrate)
time.sleep(1)

while True:
        while arduinoData.inWaiting() == 0:
            pass
        dataPacket = arduinoData.readline()
        dataPacket = str(dataPacket, 'utf-8')
        dataPacket = dataPacket.strip('\r\n')
        print(dataPacket)
