from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QPushButton, QMenu
from PyQt5.QtGui import QCursor, QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QSize
from settings_dialog import SettingsDialog

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class MenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(0, 100, 200, 200)
        self.setObjectName("menu-widget")
        self.setStyleSheet(f"""
        #menu-widget {{
            background-color: green;
        }}""")

