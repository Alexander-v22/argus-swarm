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

test_string = "Hello ESP32\r\n"
ser.reset_input_buffer(); ser.reset_output_buffer()
time.sleep(0.2)


while True: 
    n = ser.write(test_string.encode("utf-8"))
    print ("Sent", n, "bytes")
    ser.flush()
 