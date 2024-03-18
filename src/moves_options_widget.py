from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt
import math

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]
col_am = 50


class MovesOptionsList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(0, 600, 1200, 220)
        self.moves_table_layout = QGridLayout()
        self.moves_table_layout.setContentsMargins(0, 0, 0, 0)
        self.moves_table_layout.setSpacing(0)
        self.moves_table_layout.setAlignment(Qt.AlignTop)
        self.create_header(col_am)

        self.moves_widget = QWidget()
        self.moves_widget.setLayout(self.moves_table_layout)

        self.setWidget(self.moves_widget)
        self.setStyleSheet(f"""
            QScrollArea {{
                border: none;            
            }}
        
            QScrollBar:horizontal {{
                background-color: {color_theme[1]};
                color: {color_theme[3]};
                border: 1px solid {color_theme[3]}
            }}
            
            QScrollBar::handle:horizontal {{
                border: none;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
            }}
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
            {{
                background: {color_theme[3]};
                border: none;
            }}
        """)

    def create_header(self, column_amount):
        header_styles = f"""
            background-color: {color_theme[3]};
            color: {color_theme[0]};
            font-size: 18px;
        """

        divider = math.floor((self.size().width() - 150) / column_amount)
        for col in range(0, column_amount + 1):
            if col == 0:
                points_header = QLabel("Przewaga", self)
                points_header.setFixedSize(150, 40)
                points_header.setAlignment(Qt.AlignCenter)
                points_header.setStyleSheet(header_styles)
                self.moves_table_layout.addWidget(points_header, 0, col)
            else:
                move_header = QLabel(str(col), self)
                if divider < 50:
                    move_header.setFixedSize(50, 40)
                else:
                    move_header.setFixedSize(divider, 40)
                move_header.setAlignment(Qt.AlignCenter)
                move_header.setStyleSheet(header_styles)
                self.moves_table_layout.addWidget(move_header, 0, col)

    def resize_header(self, column_amount):
        divider = math.ceil((self.size().width() - 150) / column_amount)
        for col in range(1, column_amount + 1):
            if divider < 50:
                self.moves_widget.setGeometry(0, (self.size().height() - 820) + 600, (column_amount * 50) + 150, 200)
                self.moves_table_layout.itemAtPosition(0, col).widget().setFixedSize(50, 40)
            else:
                self.moves_widget.setGeometry(0, (self.size().height() - 820) + 600, (self.size().width() - 1200) + 1200, 200)
                self.moves_table_layout.itemAtPosition(0, col).widget().setFixedSize(divider, 40)

    def update_size(self, new_size):
        self.setGeometry(0, (new_size.height() - 820) + 600, (new_size.width() - 1200) + 1200, 220)
        self.resize_header(col_am)
