import cv2
from pyzbar import pyzbar
import warnings

class QRScanner:
    def __init__(self):
        self.capture = None
        self.callback = None
        self.scanning = False

    def start_scan(self, callback):
        self.callback = callback
        self.capture = cv2.VideoCapture(0)
        self.scanning = True
        self.scan()

    def stop_scan(self):
        self.scanning = False
        if self.capture is not None:
            self.capture.release()
            self.capture = None

    def scan(self):
        while self.scanning:
            ret, frame = self.capture.read()
            if ret:
                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect QR codes
                decoded_objects = pyzbar.decode(gray)

                # Process each decoded QR code
                for obj in decoded_objects:
                    # Extract the QR code data
                    qr_data = obj.data.decode("utf-8")
                    if self.callback:
                        self.callback(qr_data)

                cv2.imshow('QR Scanner', frame)
                cv2.waitKey(1)
        self.close()

    def close(self):
        cv2.destroyAllWindows()
