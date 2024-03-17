from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout, QComboBox, QSpinBox
from PyQt5.QtCore import Qt

color_theme = ["#191A19", "#1E5128", "#4E9F3D", "#D8E9A8", "#FFFFFF"]


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)

        close_btn = QPushButton("X", self)
        close_btn.setObjectName("engine-settings-close")
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setFixedSize(50, 50)
        close_btn.clicked.connect(self.close)

        bar_space = QWidget()
        bar_space.setFixedSize(450, 50)

        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignTop)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.addWidget(bar_space)
        bar_layout.addWidget(close_btn)

        close_bar = QWidget()
        close_bar.setFixedSize(500, 50)
        close_bar.setLayout(bar_layout)

        engine_label = QLabel("Silnik szachowy: ")
        elo_label = QLabel("Poziom silnika (elo): ")
        options_amount = QLabel("Ilość odpowiedzi: ")
        depth_label = QLabel("Ilość ruchów do przodu: ")
        think_time_label = QLabel("Czas przetwarzania silnika: ")
        chess_title_label = QLabel("Tytuł szachowy: ")

        engine_cb = QComboBox()
        engine_cb.addItem("Stockfish")
        engine_cb.addItem("Leela chess zero")

        elo_spinbox = QSpinBox()
        elo_spinbox.setMinimum(1000)
        elo_spinbox.setMaximum(3221)

        options_spinbox = QSpinBox()
        options_spinbox.setMinimum(1)
        options_spinbox.setMaximum(12)

        depth_spinbox = QSpinBox()
        depth_spinbox.setMinimum(1)
        depth_spinbox.setMaximum(100)

        think_cb = QComboBox()
        think_cb.addItem("1 min")
        think_cb.addItem("Bez limitu")

        chess_title_cb = QComboBox()
        chess_title_cb.addItem("None")
        chess_title_cb.addItem("Mistrz")

        grid_settings = QGridLayout()
        grid_settings.addWidget(engine_label, 1, 1)
        grid_settings.addWidget(elo_label, 2, 1)
        grid_settings.addWidget(options_amount, 3, 1)
        grid_settings.addWidget(depth_label, 4, 1)
        grid_settings.addWidget(think_time_label, 5, 1)
        grid_settings.addWidget(chess_title_label, 6, 1)
        grid_settings.setColumnMinimumWidth(1, 300)
        grid_settings.addWidget(engine_cb, 1, 2)
        grid_settings.addWidget(elo_spinbox, 2, 2)
        grid_settings.addWidget(options_spinbox, 3, 2)
        grid_settings.addWidget(depth_spinbox, 4, 2)
        grid_settings.addWidget(think_cb, 5, 2)
        grid_settings.addWidget(chess_title_cb, 6, 2)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_settings)

        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.addWidget(close_bar)
        settings_layout.addWidget(grid_widget)

        self.setObjectName("engine-setting-dialog")
        self.setFixedSize(500, 600)
        self.setLayout(settings_layout)
        self.setStyleSheet(f"""
            #engine-setting-dialog {{
                background-color: {color_theme[0]};
                border: 1px solid {color_theme[3]}; 
                border-radius: 10px; 
            }}
            
            #engine-settings-close {{
                background-color: {color_theme[0]};
                color: {color_theme[3]};
                font-size: 30px;
                border-top: 1px solid {color_theme[3]};
                border-right: 1px solid {color_theme[3]};
            }}
            
            #engine-settings-close:hover {{
                background-color: red;
                color: {color_theme[0]};
                border: 3px solid red;
            }}
            
            QLabel {{
                color: {color_theme[3]};
                font-size: 20px;
            }}
            
            QComboBox {{
                background-color: {color_theme[0]};
                color: {color_theme[3]};
                font-size: 20px;
                border: 1px solid {color_theme[3]}; 
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {color_theme[0]};
                color: {color_theme[3]};
            }}
            
            QSpinBox {{
                background-color: {color_theme[0]};
                color: {color_theme[3]};
                font-size: 20px;
                border: 1px solid {color_theme[3]}; 
            }}
            """)
