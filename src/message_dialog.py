from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from sheard_memory import SharedMemoryStorage


class MessageDialog(QDialog):
    def __init__(self, parent=None, content=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()

        self.close_btn = QPushButton("X", self)
        self.close_bar = QWidget()
        self.msg = content
        print(self.msg)

        self.set_properties()
        self.sets_layouts()

        self.msg_style = self.create_style()
        self.setStyleSheet(self.msg_style)
        self.close_btn.clicked.connect(self.close)
        
    def sets_layouts(self):
        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignRight)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.addWidget(self.close_btn)
        self.close_bar.setLayout(bar_layout)

        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(5, 5, 5, 30)
        message_layout.setAlignment(Qt.AlignTop)
        message_layout.addWidget(self.close_bar)
        message_layout.addWidget(self.msg)
        self.setLayout(message_layout)

    def set_properties(self):
        # Exit button
        self.close_btn.setObjectName("msg-close")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setFixedSize(30, 30)

        # General
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("msg-dialog")

    def create_style(self):
        return f"""
            #msg-dialog {{
                background-color: {self.storage.color_theme[1]};
                border: 1px solid {self.storage.color_theme[3]}; 
            }}

            #msg-close {{
                background-color: {self.storage.color_theme[1]};
                color: {self.storage.color_theme[3]};
                font-size: 20px;
                border: none;
            }}

            #msg-close:hover {{
                background-color: red;
                color: {self.storage.color_theme[0]};
                border: 5px solid red;
                border-radius: 10px;
            }}

            #content {{
                color: {self.storage.color_theme[3]};
                font-size: 18px;
            }}
        """

