import serial
import time  

ser = serial.Serial("/dev/serial0", 115200)

time.sleep(2)

while True: 
    received_data = ser.read()
    data_left = ser.inWaiting()
    received_data +=ser.read(data_left) # read the data on the Serial Port 
    print (received_data)
    ser.write(received_data) #transmit/ send data on Serial Port
    time.sleep(0.03)
