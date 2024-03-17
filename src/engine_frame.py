from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QPushButton, QMenu, QDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


color_theme = ["#191A19", "#1E5128", "#4E9F3D", "#D8E9A8", "#FFFFFF"]


class EngineFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Nodes elements
        sort_menu = QMenu(self)
        sort_menu.addAction("Najlepsze czarne")
        sort_menu.addAction("Najlepsze białe")
        sort_menu.addAction("Najlepsze")
        sort_menu.addAction("Najgorsze")
        sort_menu.setCursor(QCursor(Qt.PointingHandCursor))
        engine_label = QLabel("Engine: Stockfish")
        depth_label = QLabel("Depth: 20")
        moves_sort_button = QPushButton()
        moves_sort_button.setFixedSize(120, 50)
        moves_sort_button.setText("Sortowanie")
        moves_sort_button.setCursor(QCursor(Qt.PointingHandCursor))
        moves_sort_button.setMenu(sort_menu)
        engine_settings_button = QPushButton("Settings", self)
        engine_settings_button.setFixedSize(100, 50)
        engine_settings_button.setCursor(QCursor(Qt.PointingHandCursor))
        engine_settings_button.clicked.connect(self.settings_up)

        # Layouts parts
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(20, 0, 0, 0)
        left_layout.addWidget(engine_label)
        left_layout.addWidget(depth_label)
        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(moves_sort_button)
        right_layout.addWidget(engine_settings_button)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setFixedSize(250, 60)
        right_widget.setLayout(right_layout)

        # Layout
        self.engine_frame_layout = QHBoxLayout()
        self.engine_frame_layout.addWidget(left_widget)
        self.engine_frame_layout.addWidget(right_widget)
        self.engine_frame_layout.setContentsMargins(0, 0, 0, 0)
        # self.engine_frame_layout.setSpacing(1000)

        # Frame
        self.setLayout(self.engine_frame_layout)
        self.setGeometry(0, 550, 1200, 70)
        self.setObjectName("engine-frame")
        self.setStyleSheet(f"""
            #engine-frame {{
                border-top: 1px solid {color_theme[3]};
                border-bottom: 1px solid {color_theme[3]};
            }}
                
            QWidget {{
                color: {color_theme[3]};
                font-size: 20px;
            }}
            
            QPushButton {{
                border: 1px solid {color_theme[3]};
                border-radius: 10px;
            }}
            
            QPushButton::menu-indicator {{
                image: none;
                width: 0px;
            }}
            
            QPushButton:hover {{
                color: black;
                background-color: {color_theme[3]};
            }}
            
            QMenu {{
                width: 200px;
                padding-top: 5px; 
                color: {color_theme[3]};
                background-color: {color_theme[0]};
                border: 1px solid {color_theme[3]};
                border-radius: 10px;
            }}
            
            QMenu::item {{
                padding: 10px 30px;
            }}
            
            QMenu::item:selected {{
                color: {color_theme[0]};
                background-color: {color_theme[3]};
            }}
            """)

    def change_for_window_resize(self, new_size):
        self.engine_frame_layout.setSpacing(400 + new_size.width()-1200)
        self.setGeometry(0, (new_size.height() - 820) + 550, (new_size.width() - 1200) + 1200, 70)

    def settings_up(self):
        print("Clicked")

        setting_window = QDialog()
        # setting_window.setWindowTitle("Settings")
        setting_window.setWindowFlag(Qt.FramelessWindowHint)
        btn = QPushButton("Close", setting_window)
        btn.clicked.connect(setting_window.close)

        la = QHBoxLayout()
        la.addWidget(btn)
        setting_window.setLayout(la)
        setting_window.exec()

