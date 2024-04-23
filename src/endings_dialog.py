from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from engine import ChessEngine
from sheard_memory import SharedMemoryStorage


class EndingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()

        # Items
        self.close_btn = QPushButton("X", self)
        self.dialog_title = QLabel("Końcówki szachowe")
        self.bar_space = QWidget()
        self.close_bar = QWidget()
        self.content_widget = QWidget()

        # Creating container
        self.set_items_properties()
        self.set_layouts()
        self.set_general_properties()
        self.save_style = self.create_style()
        self.setStyleSheet(self.save_style)
        self.assign_actions()

    def assign_actions(self):
        self.close_btn.clicked.connect(self.close)

    def set_general_properties(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("endings-dialog")
        self.setFixedSize(800, 600)

    def set_layouts(self):
        # Dialog title
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.dialog_title)
        self.bar_space.setLayout(title_layout)

        # Top bar
        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignTop)
        bar_layout.setContentsMargins(0, 0, 5, 0)
        bar_layout.addWidget(self.bar_space)
        bar_layout.addWidget(self.close_btn)
        self.close_bar.setLayout(bar_layout)

        # Content
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignVCenter)
        content_layout.setContentsMargins(40, 10, 40, 10)
        self.content_widget.setLayout(content_layout)

        # General
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setAlignment(Qt.AlignTop)
        settings_layout.addWidget(self.close_bar)
        settings_layout.addWidget(self.content_widget)
        self.setLayout(settings_layout)

    def set_items_properties(self):
        # Close
        self.close_btn.setObjectName("endings-close")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setFixedSize(30, 30)

        # Labels
        self.dialog_title.setStyleSheet(f"color: {self.storage.color_theme[3]};font-size: 18px;")

    def update_style(self):
        style = self.create_style()
        self.setStyleSheet(style)

    def create_style(self):
        return f"""
               #endings-dialog {{
                   background-color: {self.storage.color_theme[0]};
                   border: 1px solid {self.storage.color_theme[3]}; 
               }}

               #endings-close {{
                   background-color: {self.storage.color_theme[0]};
                   color: {self.storage.color_theme[3]};
                   font-size: 20px;
                   border: none;
               }}

               #endings-close:hover {{
                   background-color: red;
                   color: {self.storage.color_theme[0]};
                   border: 5px solid red;
                   border-radius: 10px;
               }}
        """