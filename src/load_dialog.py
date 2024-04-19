from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from engine import ChessEngine
from sheard_memory import SharedMemoryStorage


class LoadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = ChessEngine()
        self.storage = SharedMemoryStorage()
        self.setWindowFlag(Qt.FramelessWindowHint)

        close_btn = QPushButton("X", self)
        close_btn.setObjectName("engine-settings-close")
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)

        dialog_title = QLabel("Wczytaj partię")
        title_layout = QHBoxLayout()
        title_layout.addWidget(dialog_title)

        bar_space = QWidget()
        bar_space.setFixedSize(380, 40)
        bar_space.setLayout(title_layout)

        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignTop)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.addWidget(bar_space)
        bar_layout.addWidget(close_btn)

        close_bar = QWidget()
        close_bar.setFixedSize(420, 40)
        close_bar.setLayout(bar_layout)
        close_bar.setObjectName("engine_title")

        grid_settings = QGridLayout()
        grid_settings.setColumnMinimumWidth(1, 300)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_settings)

        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(0, 0, 20, 0)
        settings_layout.addWidget(close_bar)
        settings_layout.addWidget(grid_widget)

        self.setObjectName("engine-setting-dialog")
        self.setFixedSize(420, 600)
        self.setLayout(settings_layout)
        self.setStyleSheet(f"""
            #engine-setting-dialog {{
                background-color: {self.storage.color_theme[0]};
                border: 1px solid {self.storage.color_theme[3]}; 
            }}

            #engine-settings-close {{
                background-color: {self.storage.color_theme[0]};
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

            #engine_title {{
                border-bottom: 1px solid {self.storage.color_theme[3]};
            }}

            QLabel {{
                color: {self.storage.color_theme[3]};
                font-size: 18px;
            }}

            QComboBox {{
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
                font-size: 18px;
                border: 1px solid {self.storage.color_theme[3]}; 
            }}

            QComboBox QAbstractItemView {{
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
            }}

            QSpinBox {{
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
                font-size: 18px;
                border: 1px solid {self.storage.color_theme[3]}; 
            }}
            """)