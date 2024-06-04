from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QLineEdit,QDialog
from PyQt5.QtCore import Qt
from camera import CameraWidget
import database

class LoginForm(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Form")
        self.setGeometry(100, 100, 400, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Top Container (Face Capture)
        top_container = QFrame()
        top_container.setFixedHeight(200)
        top_container.setStyleSheet("background-color: #f2f2f2; border: 3px solid black; border-radius: 7px; ")
        main_layout.addWidget(top_container)

        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(20, 20, 20, 20)

        self.camera_widget = CameraWidget()
        top_layout.addWidget(self.camera_widget)

        # Middle Container (Worker ID)
        middle_container = QFrame()
        middle_container.setFixedHeight(200)
        middle_container.setStyleSheet("background-color: #f2f2f2; border: 3px solid black; border-radius: 7px; ")
        main_layout.addWidget(middle_container)

        middle_layout = QHBoxLayout(middle_container)
        middle_layout.setContentsMargins(20, 20, 20, 20)

        worker_id_label = QLabel("Worker ID:", middle_container)
        worker_id_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        middle_layout.addWidget(worker_id_label)

        self.worker_id_line_edit = QLineEdit(middle_container)
        middle_layout.addWidget(self.worker_id_line_edit)
        
        # Bottom Container (Capture Button)
        bottom_container = QFrame()
        bottom_container.setFixedHeight(200)
        bottom_container.setStyleSheet("background-color: #f2f2f2; border: 3px solid black; border-radius: 7px; ")
        main_layout.addWidget(bottom_container)

        bottom_layout = QHBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setAlignment(Qt.AlignCenter)

        capture_button = QPushButton("LOGIN", bottom_container)
        capture_button.setStyleSheet("QPushButton { background-color: #f2f2f2; font-size: 25px; font-weight: bold; }"
                                      "QPushButton:hover { background-color: green; }")
        capture_button.clicked.connect(self.capture_clicked)
        bottom_layout.addWidget(capture_button)

    def clear_form(self):
        self.worker_id_line_edit.clear()

    def get_worker_id(self):
        return self.worker_id_line_edit.text()

    def capture_clicked(self):
        worker_id = self.worker_id_line_edit.text()
        self.camera_widget.capture_face(worker_id)
        if worker_id:
            self.accept()
