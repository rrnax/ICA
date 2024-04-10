from PyQt5.QtGui import QCursor, QIcon, QPixmap, QTransform
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt, QSize
from logic_board import LogicBoard
color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class SideDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.logic_board = LogicBoard()

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

        white_knight = QPixmap("../resources/pieces/w_knight.png")
        white_knight = white_knight.scaled(QSize(80, 80), transformMode=Qt.SmoothTransformation)

        black_knight = QPixmap("../resources/pieces/b_knight.png")
        black_knight = black_knight.transformed(QTransform().scale(-1, 1))
        black_knight = black_knight.scaled(QSize(80, 80), transformMode=Qt.SmoothTransformation)

        white_label = QLabel("Białe")
        white_label.setFixedSize(100, 20)
        white_label.setAlignment(Qt.AlignCenter)
        black_label = QLabel("Czarne")
        black_label.setFixedSize(100, 20)
        black_label.setAlignment(Qt.AlignCenter)

        white_button = QPushButton()
        white_button.setFixedSize(100, 100)
        white_button.setIcon(QIcon(white_knight))
        white_button.setIconSize(white_knight.size())
        white_button.setCursor(Qt.PointingHandCursor)

        black_button = QPushButton()
        black_button.setFixedSize(100, 100)
        black_button.setIcon(QIcon(black_knight))
        black_button.setIconSize(black_knight.size())
        black_button.setCursor(Qt.PointingHandCursor)

        layout = QGridLayout()
        layout.setContentsMargins(10, 0, 10, 10)
        layout.addWidget(white_label, 1, 1)
        layout.addWidget(black_label, 1, 2)
        layout.addWidget(white_button, 2, 1)
        layout.addWidget(black_button, 2, 2)

        widget = QWidget()
        widget.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color_theme[1]};
                        border: 1px solid {color_theme[1]};
                    }}

                    QPushButton:hover {{
                        background-color: {color_theme[3]};
                        border-radius: 10px;
                    }}
                    """)
        widget.setLayout(layout)

        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(5, 5, 5, 5)
        message_layout.setAlignment(Qt.AlignTop)
        message_layout.addWidget(close_bar)
        message_layout.addWidget(widget)

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
        white_button.clicked.connect(self.set_white)
        black_button.clicked.connect(self.set_black)

    def set_white(self):
        self.logic_board.player_side = "white"
        self.close()

    def set_black(self):
        self.logic_board.player_side = "black"
        self.close()

