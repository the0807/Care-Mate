import serial
import time

port = '/dev/ttyUSB0'
baudrate = 9600

arduino = serial.Serial(port, baudrate)
time.sleep(2)

value = "TEST"

arduino.write(str(value).encode())
print('값 전송 완료:', value)

arduino.close()