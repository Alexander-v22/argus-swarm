import serial
import time  

ser = serial.Serial(
    "/dev/ttyAMA0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,
    rtscts=False,   # make sure HW flow control is OFF
    dsrdtr=False,
    xonxoff=False   # and SW flow control is OFF
)

#test_string = "Hello ESP32\r\n"
time.sleep(0.2)
ser.reset_input_buffer()
ser.reset_output_buffer()

#setting Data Terminal Ready and Request to Send high
ser.setDTR(True)
ser.setRTS(True)


for i in range(5):
    ser.write(b"ping %d\n" % i)
    ser.flush()
    time.sleep(0.1)
    data = ser.read(64)              # <-- actually read it back
    print("wrote ping %d, read:" % i, data)