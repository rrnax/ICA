from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class MessageDialog(QDialog):
    def __init__(self, parent=None, content=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)

        close_btn = QPushButton("X", self)
        close_btn.setObjectName("engine-settings-close")
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setFixedSize(30, 30)

        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignRight)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.addWidget(close_btn)

        close_bar = QWidget()
        close_bar.setLayout(bar_layout)

        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(5, 5, 5, 5)
        message_layout.setAlignment(Qt.AlignTop)
        message_layout.addWidget(close_bar)
        message_layout.addWidget(content)

        self.setObjectName("engine-setting-dialog")
        # self.setFixedSize(200, 100)
        self.setLayout(message_layout)
        self.setStyleSheet(f"""
            #engine-setting-dialog {{
                background-color: {color_theme[1]};
                border: 1px solid {color_theme[3]}; 
            }}

            #engine-settings-close {{
                background-color: {color_theme[1]};
                color: {color_theme[3]};
                font-size: 20px;
                border: none;
            }}

            #engine-settings-close:hover {{
                background-color: red;
                color: {color_theme[0]};
                border: 5px solid red;
                border-radius: 10px;
            }}

            QLabel {{
                color: {color_theme[3]};
                font-size: 18px;
            }}
            """)

        close_btn.clicked.connect(self.close)


