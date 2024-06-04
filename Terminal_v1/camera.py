import cv2
import os
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer,Qt

class CameraWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(360, 160)
        self.setAlignment(Qt.AlignCenter)

        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
            self.setPixmap(pixmap)

    def capture_face(self, worker_id):
        ret, frame = self.capture.read()
        if ret:
            save_folder = r"C:/Users/Admin/Documents/Terminal_v1/Worker_image"
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, f"{worker_id}.png")
            cv2.imwrite(save_path, frame)
