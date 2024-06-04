import serial

# Configure serial communication with Arduino
arduino_port = 'COM6'  # Replace with the correct port for your Arduino
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

# Read data from Arduino
def detect_rfid():
    while True:
        if ser.in_waiting:
            data = ser.readline().decode().strip()
            parts = data.split(":")
            if len(parts) > 1:
                rfid = parts[1].strip()
                print(rfid)
                return True, rfid