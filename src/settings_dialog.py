from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
from engine import ChessEngine

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.engine = ChessEngine()

        close_btn = QPushButton("X", self)
        close_btn.setObjectName("engine-settings-close")
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)

        dialog_title = QLabel("Ustawienia silnika szachowego")
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

        engine_label = QLabel("Silnik szachowy: ")
        engine_label.setAlignment(Qt.AlignRight)
        elo_label = QLabel("Poziom silnika (elo): ")
        elo_label.setAlignment(Qt.AlignRight)
        options_amount = QLabel("Ilość odpowiedzi: ")
        options_amount.setAlignment(Qt.AlignRight)
        depth_label = QLabel("Ilość ruchów do przodu: ")
        depth_label.setAlignment(Qt.AlignRight)
        think_time_label = QLabel("Czas przetwarzania: ")
        think_time_label.setAlignment(Qt.AlignRight)
        chess_title_label = QLabel("Tytuł szachowy: ")
        chess_title_label.setAlignment(Qt.AlignRight)

        self.engine_cb = QComboBox()
        self.engine_cb.addItem("Stockfish")
        self.engine_cb.addItem("Leela chess zero")

        self.elo_spinbox = QSpinBox()
        self.elo_spinbox.setMinimum(100)
        self.elo_spinbox.setMaximum(3221)

        self.options_spinbox = QSpinBox()
        self.options_spinbox.setMinimum(1)
        self.options_spinbox.setMaximum(12)

        self.depth_spinbox = QSpinBox()
        self.depth_spinbox.setMinimum(1)
        self.depth_spinbox.setMaximum(100)

        self.think_cb = QComboBox()
        self.think_cb.addItem("Bez limitu")
        self.think_cb.addItem("20 s")
        self.think_cb.addItem("30 s")
        self.think_cb.addItem("40 s")
        self.think_cb.addItem("50 s")
        for i in range(1, 60):
            self.think_cb.addItem(str(i) + " min")

        self.chess_title_cb = QComboBox()
        self.chess_title_cb.addItem("None")
        self.chess_title_cb.addItem("GM")
        self.chess_title_cb.addItem("IM")

        grid_settings = QGridLayout()
        grid_settings.addWidget(engine_label, 1, 1)
        grid_settings.addWidget(elo_label, 2, 1)
        grid_settings.addWidget(options_amount, 3, 1)
        grid_settings.addWidget(depth_label, 4, 1)
        grid_settings.addWidget(think_time_label, 5, 1)
        grid_settings.addWidget(chess_title_label, 6, 1)
        grid_settings.setColumnMinimumWidth(1, 300)
        grid_settings.addWidget(self.engine_cb, 1, 2)
        grid_settings.addWidget(self.elo_spinbox, 2, 2)
        grid_settings.addWidget(self.options_spinbox, 3, 2)
        grid_settings.addWidget(self.depth_spinbox, 4, 2)
        grid_settings.addWidget(self.think_cb, 5, 2)
        grid_settings.addWidget(self.chess_title_cb, 6, 2)

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
                background-color: {color_theme[0]};
                border: 1px solid {color_theme[3]}; 
            }}
            
            #engine-settings-close {{
                background-color: {color_theme[0]};
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
            
            #engine_title {{
                border-bottom: 1px solid {color_theme[3]};
            }}
            
            QLabel {{
                color: {color_theme[3]};
                font-size: 18px;
            }}
            
            QComboBox {{
                background-color: {color_theme[0]};
                color: {color_theme[3]};
                font-size: 18px;
                border: 1px solid {color_theme[3]}; 
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {color_theme[0]};
                color: {color_theme[3]};
            }}
            
            QSpinBox {{
                background-color: {color_theme[0]};
                color: {color_theme[3]};
                font-size: 18px;
                border: 1px solid {color_theme[3]}; 
            }}
            """)
        self.elo_spinbox.valueChanged.connect(self.change_elo)
        self.options_spinbox.valueChanged.connect(self.change_amount)
        self.depth_spinbox.valueChanged.connect(self.change_depth)
        self.think_cb.currentTextChanged.connect(self.change_time)
        self.chess_title_cb.currentTextChanged.connect(self.change_title)
        self.engine_cb.currentTextChanged.connect(self.change_engine)

    def change_engine(self):
        engine = self.engine_cb.currentText()
        self.engine.set_engine(engine)

    def change_elo(self):
        elo = self.elo_spinbox.value()
        self.engine.set_elo(elo)

    def change_amount(self):
        amount = self.options_spinbox.value()
        self.engine.set_amount_moves(amount)

    def change_depth(self):
        depth = self.depth_spinbox.value()
        self.engine.set_depth(depth)

    def change_time(self):
        time_txt = self.think_cb.currentText()
        if "min" in time_txt:
            substrings = time_txt.split()
            self.engine.set_time(60 * int(substrings[0]))
        elif time_txt == "Bez limitu":
            result = None
            self.engine.set_time(result)
        else:
            substrings = time_txt.split()
            self.engine.set_time(int(substrings[0]))

    def change_title(self):
        title = self.chess_title_cb.currentText()
        self.engine.set_title(title)

    # def starting_parametrs(self):







