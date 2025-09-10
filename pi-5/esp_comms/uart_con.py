import serial
import time  

ser = serial.Serial("/dev/ttyAMA10", 115200)

time.sleep(2)

while true: 
    received_data = ser.read()
    sleep(0.03)
    data_left = ser.inWaiting()
    received_data +=ser.read(data_left) # read the data on the Serial Port 
    print (received_data)
    ser.write(received_data) #transmit/ send data on Serial Port