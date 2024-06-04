from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,QGridLayout,QMessageBox,QDialog
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPixmap
import database
from login_form import LoginForm
import sys
from qr_scanner import QRScanner
from rfid import detect_rfid,ser
import threading
import definition

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Layout")
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.username_label = QLabel()  # Add username label
        self.position_label = QLabel()  # Add position label

        # Title Container
        title_container = QFrame()
        title_container.setFixedHeight(100)  # Set the desired height
        title_container.setStyleSheet("background-color: #f2f2f2; border: 3px solid black; border-radius: 7px; ")

        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)  # Remove the default margin

        # Title
        title_label = QLabel("TERMINAL (MACHINING)")
        title_label.setAlignment(Qt.AlignCenter)  # Align label text to the center
        title_label.setStyleSheet("font-size: 25px; font-weight: bold;")
        title_layout.addWidget(title_label)

        # Add the title container to the main layout
        main_layout.addWidget(title_container)

        # Sub-layouts
        sub_layout = QHBoxLayout()
        main_layout.addLayout(sub_layout)

        # Left Side
        left_box = QVBoxLayout()
        left_box.setContentsMargins(0, 0, 0, 0)  # Remove the default margin
        left_container = QWidget()
        left_container.setLayout(left_box)
        left_container.setFixedWidth(200)
        left_container.setStyleSheet("border: 5px solid black; border-radius: 7px;")
        sub_layout.addWidget(left_container)

        login_button = QPushButton("Login")
        login_button.setStyleSheet("QPushButton { background-color: #f2f2f2; font-size: 40px; font-weight: bold; }"
                                    "QPushButton:hover { background-color: green; }")
        login_button.setFixedSize(200, 427)  # Set the button size
        login_button.clicked.connect(self.show_login_form)
        left_box.addWidget(login_button, 1)  # Set stretch factor to 1

        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("QPushButton { background-color: #f2f2f2; font-size: 40px; font-weight: bold; }" 
                                    "QPushButton:hover { background-color: red; }")
        logout_button.setFixedSize(200,425)  # Set the button size
        left_box.addWidget(logout_button, 1)  # Set stretch factor to 1
        
        # Right Side
        right_grid_layout = QGridLayout()
        right_grid_layout.setContentsMargins(20, 10, 20, 10)
        right_container = QWidget()
        right_container.setLayout(right_grid_layout)
        right_container.setStyleSheet("border: 5px solid black; border-radius: 7px;")
        sub_layout.addWidget(right_container)

        # User Profile box
        User_Profile_box = QWidget()
        User_Profile_box.setFixedSize(400, 400)
        User_Profile_box.setStyleSheet("border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(User_Profile_box, 0, 0)
        
        self.user_image_label = QLabel(User_Profile_box)
        self.user_image_label.setScaledContents(True)
        self.user_image_label.setGeometry(10, 10, 380, 380)

        # WorkOrder Picture container
        Job_box = QWidget()
        Job_box.setFixedSize(400, 400)
        Job_box.setStyleSheet("border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(Job_box, 0, 1)
        
        self.workorder_image_label = QLabel(Job_box)
        self.workorder_image_label.setScaledContents(True)
        self.workorder_image_label.setGeometry(10, 10, 380, 380)
        
        #User Name
        Username_box = QWidget()
        Username_box.setStyleSheet("background-color: #f2f2f2; border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(Username_box, 1, 0)
        
        Username_box_label = QLabel("Username", Username_box)
        Username_box_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        Username_box_label.setGeometry(10, 5, 350, 50)
        Username_box_label.setStyleSheet("border:none; font-size: 30px; font-weight: bold; ")
        
        self.username_name = QLabel("", Username_box)
        self.username_name.setAlignment(Qt.AlignCenter)
        self.username_name.setGeometry(120,70,180,90)
        self.username_name.setStyleSheet("border:none; font-size: 25px; font-weight: bold ")

        #Position 
        Position_box = QWidget()
        Position_box.setStyleSheet("background-color: #f2f2f2; border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(Position_box, 2, 0)
        
        Position_box_label = QLabel("User Position", Position_box)
        Position_box_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        Position_box_label.setGeometry(10, 5, 350, 50)
        Position_box_label.setStyleSheet("border:none; font-size: 30px; font-weight: bold; ")
        
        self.Position = QLabel("", Position_box)
        self.Position.setAlignment(Qt.AlignCenter)
        self.Position.setGeometry(90,70,250,90)
        self.Position.setStyleSheet("border:none; font-size: 25px; font-weight: bold ")
        
        #Work Order
        WorkOrder_box = QWidget()
        WorkOrder_box.setStyleSheet("background-color: #f2f2f2; border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(WorkOrder_box, 1, 2)
        
        WorkOrder_box_label = QLabel("Work Order", WorkOrder_box)
        WorkOrder_box_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        WorkOrder_box_label.setGeometry(10, 5, 350, 50)
        WorkOrder_box_label.setStyleSheet("border:none; font-size: 30px; font-weight: bold; ")
        
        self.workorder = QLabel("", WorkOrder_box)
        self.workorder.setAlignment(Qt.AlignCenter)
        self.workorder.setGeometry(120,70,180,90)
        self.workorder.setStyleSheet("border:none; font-size: 25px; font-weight: bold ")
        
        #Scan Work Order
        ScanWorkOrder_box = QWidget()
        ScanWorkOrder_box.setStyleSheet("background-color: #f2f2f2; border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(ScanWorkOrder_box, 1, 3)
        
        ScanWorkOrder_button = QPushButton("SCAN QR",ScanWorkOrder_box)
        ScanWorkOrder_button.setStyleSheet("QPushButton { background-color: #f2f2f2; font-size: 40px; font-weight: bold; border:none; }"
                                    "QPushButton:hover { background-color: blue; }")
        ScanWorkOrder_button.setGeometry(35,30,350,150)
        
        self.qr_scanner = QRScanner()
        ScanWorkOrder_button.clicked.connect(self.start_qr_scanning)
        
        #Part Number
        PartNumber_box = QWidget()
        PartNumber_box.setStyleSheet("background-color: #f2f2f2; border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(PartNumber_box, 2, 1)
        
        PartNumber_box_label = QLabel("Part Number", PartNumber_box)
        PartNumber_box_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        PartNumber_box_label.setGeometry(10, 5, 350, 50)
        PartNumber_box_label.setStyleSheet("border:none; font-size: 30px; font-weight: bold; ")
        
        self.partnumber = QLabel("", PartNumber_box)
        self.partnumber.setAlignment(Qt.AlignCenter)
        self.partnumber.setGeometry(120,70,180,90)
        self.partnumber.setStyleSheet("border:none; font-size: 25px; font-weight: bold ")

        #Timer
        Timer_box = QWidget()
        Timer_box.setStyleSheet("background-color: #f2f2f2; border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(Timer_box, 2, 2)
        
        Timer_box_label = QLabel("Time", Timer_box)
        Timer_box_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        Timer_box_label.setGeometry(10, 5, 350, 50)
        Timer_box_label.setStyleSheet("border:none; font-size: 30px; font-weight: bold; ")
        
        self.timer_label = QLabel("", Timer_box)  
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setGeometry(120, 70, 180, 90)
        self.timer_label.setStyleSheet("border:none; font-size: 25px; font-weight: bold ")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)  # Connect the timeout signal to the update_timer method

        #Job Order
        JobOrder_box = QWidget()
        JobOrder_box.setStyleSheet("background-color: #f2f2f2; border: 5px solid black; border-radius: 7px;")
        right_grid_layout.addWidget(JobOrder_box, 1, 1)
        
        JobOrder_box_label = QLabel("Job Order", JobOrder_box)
        JobOrder_box_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        JobOrder_box_label.setGeometry(10, 5, 350, 50)
        JobOrder_box_label.setStyleSheet("border:none; font-size: 30px; font-weight: bold; ")
        
        self.joborder = QLabel("", JobOrder_box)
        self.joborder.setAlignment(Qt.AlignCenter)
        self.joborder.setGeometry(120,70,180,90)
        self.joborder.setStyleSheet("border:none; font-size: 25px; font-weight: bold ")

        right_grid_layout.setColumnStretch(0, 1)  # Allow column 0 to stretch
        
        # Create an instance of the login form
        self.login_form = LoginForm()
        
        # Create a thread for RFID detection
        self.rfid_thread = None

        # Connect the login button to show the login form
        #login_button.clicked.connect(self.show_login_form)

        # Connect the logout button to hide the login form
        logout_button.clicked.connect(self.hide_login_form)

        # Initially hide the login form
        self.login_form.hide()
        
    
    def show_login_form(self):
        if not self.login_form.isVisible():  # Check if the login form is already visible
            self.login_form.clear_form()
            result = self.login_form.exec_()
            if result == QDialog.Accepted:
                worker_id = self.login_form.get_worker_id()
                user_info = database.retrieve_user_info(worker_id)
                if user_info:
                    username, position = user_info
                    self.update_user_profile(username, position, worker_id)
                else:
                    self.update_user_profile("User Not Found", "N/A")

    def update_user_profile(self, username, position, worker_id):
        self.username_name.setText(username)
        self.Position.setText(position)
        
        pixmap = QPixmap(f'C:/Users/Admin/Documents/Terminal_v1/Worker_Image/{worker_id}.png')
        self.user_image_label.setPixmap(pixmap)
        
    def hide_login_form(self):
        self.login_form.hide()   
        
    def start_qr_scanning(self):
        self.qr_scanner.start_scan(self.process_qr_data)

    def process_qr_data(self, qr_data):
        self.stop_qr_scanning(qr_data)
        self.start_rfid_detection_thread()
    
    def start_rfid_detection_thread(self):
        # Create a new thread for RFID detection
        self.rfid_thread = threading.Thread(target=self.handle_rfid_detection)
        self.rfid_thread.start()

    def handle_rfid_detection(self):
         success, rfid = detect_rfid()
         if success:
             workorder = self.workorder.text()
             workorder_info = database.retrieve_work_order_info(workorder)
            
             WorkOrder, JobOrder, PartNumber,CycleTime = workorder_info
             terminal = definition.IDENTITY
             status = definition.STATUS_DONE
             workerid = self.login_form.get_worker_id()
            
             database.insert_rfid_workorder_info(WorkOrder, JobOrder, PartNumber, CycleTime, status, rfid, terminal, workerid)
             # Clear the work order information
             self.workorder.setText("")
             self.joborder.setText("")
             self.partnumber.setText("")
             self.timer_label.setText("")
             self.workorder_image_label.clear()
            
             if self.timer.isActive():
                 self.timer.stop()
                
         else:
             QMessageBox.information(self, "RFID Error", "Failed to detect RFID")

    def stop_qr_scanning(self, qr_data):
        self.qr_scanner.stop_scan()
        workorder_info = database.retrieve_work_order_info(qr_data)
        if workorder_info:
            WorkOrder, JobOrder, PartNumber, CycleTime = workorder_info
            self.update_order_profile(WorkOrder,JobOrder,PartNumber,CycleTime)
        else:
            QMessageBox.information(self, "Error", "Work Order not Found")

    def update_order_profile(self, WorkOrder, JobOrder, PartNumber, CycleTime):
        self.workorder.setText(WorkOrder)
        self.partnumber.setText(PartNumber)
        self.joborder.setText(JobOrder)
        
        pixmap = QPixmap(f'C:/Users/Admin/Documents/Terminal_v1/WorkOrder_Image/{WorkOrder}.png')
        self.workorder_image_label.setPixmap(pixmap)
        # Set the initial countdown time
        self.current_time = CycleTime*60
        self.update_timer()  # Update the timer display

        # Start the countdown timer
        self.timer.start(1000)  # Update every second (1000 ms)
        
    def update_timer(self):
        if self.current_time > 0:
            self.current_time -= 1
            seconds = self.current_time % 60
            minutes = (self.current_time // 60) % 60
            hours = (self.current_time // 3600) % 24
            self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.timer.stop()
            self.timer_label.setText("Timer finished!")
        
    def closeEvent(self, event):
        self.stop_qr_scanning()
        ser.close()
        super().closeEvent(event)
       
        
        
if __name__ == "__main__":
    
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    
    sys.exit(app.exec_())
