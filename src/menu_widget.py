from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QPushButton, QMenu, QVBoxLayout
from PyQt5.QtGui import QCursor, QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from settings_dialog import SettingsDialog

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class MenuSlideFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        hide_btn = QPushButton()

        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(hide_btn)

        # General sets for menu
        self.animation = QPropertyAnimation(self, b"geometry", self)
        self.setGeometry(-400, 0, 400, 820)
        self.setLayout(menu_layout)
        self.setObjectName("menu-slide-frame")
        self.setStyleSheet(f"""
        #menu-slide-frame {{
            background-color: {color_theme[0]};
            border-right: 1px solid {color_theme[3]}; 
        }}
        """)

        # Actions
        hide_btn.clicked.connect(self.close_menu)

    # Show or hide menu
    def open_menu(self):
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(-400, 0, 400, 820))
        self.animation.setEndValue(QRect(0, 0, 400, 820))
        self.animation.start()

    def close_menu(self):
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(0, 0, 400, 820))
        self.animation.setEndValue(QRect(-400, 0, 400, 820))
        self.animation.start()

    # For window change
    def update_size(self, new_size):
        self.setFixedSize(400, (new_size.height() - 820) + 820)
