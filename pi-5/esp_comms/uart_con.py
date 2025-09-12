import serial
import time  

ser = serial.Serial("/dev/serial0", 115200, timeout = 1)

ser.reset_input_buffer()
time.sleep(0.2)

while True: 
    n = ser.in_waiting  # how many bytes are buffered better than old code where we expected one byte
    if n:
        received_data = ser.read(n)  # read all available bytes
        print(received_data.decode(errors="replace").strip())
        ser.write(received_data)     # echo back
    time.sleep(0.03)