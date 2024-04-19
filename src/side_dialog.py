from PyQt5.QtGui import QCursor, QIcon, QPixmap, QTransform
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt, QSize
from logic_board import LogicBoard
from sheard_memory import SharedMemoryStorage


class SideDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()
        self.logic_board = LogicBoard()

        # Elements
        self.close_btn = QPushButton("X", self)
        self.close_bar = QWidget()
        self.white_label = QLabel("Białe")
        self.black_label = QLabel("Czarne")
        self.white_button = QPushButton()
        self.black_button = QPushButton()
        self.equal_widget = QWidget()
        self.sides_style = self.create_style()


        # Pieces to choose pictures
        self.white_knight = QPixmap("../resources/pieces/w_knight.png")
        self.white_knight = self.white_knight.scaled(QSize(80, 80), transformMode=Qt.SmoothTransformation)
        self.black_knight = QPixmap("../resources/pieces/b_knight.png")
        self.black_knight = self.black_knight.transformed(QTransform().scale(-1, 1))
        self.black_knight = self.black_knight.scaled(QSize(80, 80), transformMode=Qt.SmoothTransformation)

        # Creating message content
        self.set_items_properties()
        self.set_general_properties()
        self.set_layouts()
        self.setStyleSheet(self.sides_style)
        self.assign_actions()

    # Connect action to buttons
    def assign_actions(self):
        self.close_btn.clicked.connect(self.close)
        self.white_button.clicked.connect(self.set_white)
        self.black_button.clicked.connect(self.set_black)

    def set_general_properties(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("engine-setting-dialog")
        
    def set_items_properties(self):
        # Close
        self.close_btn.setObjectName("engine-settings-close")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setFixedSize(30, 30)
        
        # Descriptive labels
        self.white_label.setFixedSize(100, 20)
        self.white_label.setAlignment(Qt.AlignCenter)
        self.black_label.setFixedSize(100, 20)
        self.black_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.white_button.setFixedSize(100, 100)
        self.white_button.setIcon(QIcon(self.white_knight))
        self.white_button.setIconSize(self.white_knight.size())
        self.white_button.setCursor(Qt.PointingHandCursor)
        self.black_button.setFixedSize(100, 100)
        self.black_button.setIcon(QIcon(self.black_knight))
        self.black_button.setIconSize(self.black_knight.size())
        self.black_button.setCursor(Qt.PointingHandCursor)

    def set_layouts(self):
        # Bar on the top
        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignRight)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.addWidget(self.close_btn)
        self.close_bar.setLayout(bar_layout)

        # For equal elements layout
        layout = QGridLayout()
        layout.setContentsMargins(10, 0, 10, 10)
        layout.addWidget(self.white_label, 1, 1)
        layout.addWidget(self.black_label, 1, 2)
        layout.addWidget(self.white_button, 2, 1)
        layout.addWidget(self.black_button, 2, 2)
        self.equal_widget.setLayout(layout)

        # General
        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(5, 5, 5, 5)
        message_layout.setAlignment(Qt.AlignTop)
        message_layout.addWidget(self.close_bar)
        message_layout.addWidget(self.equal_widget)
        self.setLayout(message_layout)

    # Choose actions
    def set_white(self):
        self.logic_board.player_side = "white"
        self.close()

    def set_black(self):
        self.logic_board.player_side = "black"
        self.close()

    def set_close(self):
        self.logic_board.player_side = None
        self.close()

    # Styles making
    def create_style(self):
        return f"""
            #engine-setting-dialog {{
                background-color: {self.storage.color_theme[1]};
                border: 1px solid {self.storage.color_theme[3]}; 
            }}

            #engine-settings-close {{
                background-color: {self.storage.color_theme[1]};
                color: {self.storage.color_theme[3]};
                font-size: 20px;
                border: none;
            }}

            #engine-settings-close:hover {{
                background-color: red;
                color: {self.storage.color_theme[0]};
                border: 5px solid red;
                border-radius: 10px;
            }}

            QLabel {{
                color: {self.storage.color_theme[3]};
                font-size: 18px;
            }}
            
            QPushButton {{
                        background-color: {self.storage.color_theme[1]};
                        border: 1px solid {self.storage.color_theme[1]};
                    }}

            QPushButton:hover {{
                background-color: {self.storage.color_theme[3]};
                border-radius: 10px;
            }}
            """
