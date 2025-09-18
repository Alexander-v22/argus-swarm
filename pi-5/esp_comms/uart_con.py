import serial
import time  

class ESP32UART:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout=1):
        ser = serial.Serial(
            "/dev/ttyAMA0",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            rtscts=False,   
            dsrdtr=False,
            xonxoff=False   
        )

        # need these for my UART connection to work 
        time.sleep(0.2)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        #setting Data Terminal Ready and Request to Send high like the MINICOM work space
        ser.setDTR(True)
        ser.setRTS(True)

        # self --> refrence to the object itself
        def send_angles (self, pan, tilt):
            msg = f"{int(pan)},{int(tilt)}\n"
            self.ser.write(msg.encode)
            self.ser.flush() # forces any data lingering in the output buffer to be sent immediately through the serial port

        def close(self):
            self.ser.flush()