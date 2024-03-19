from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import math

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]
col_am = 20
moves = ["+1,922", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2",
         "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2",  "a1b2", "a1b2",
         "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2"]
rA = 4


class MovesOptionsList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pieces = [QPixmap("../resources/pieces/b_bishop.png"),
          QPixmap("../resources/pieces/b_king.png").scaled(20, 20),
          QPixmap("../resources/pieces/b_knight.png").scaled(20, 20),
          QPixmap("../resources/pieces/b_pawn.png").scaled(20, 20),
          QPixmap("../resources/pieces/b_queen.png").scaled(20, 20),
          QPixmap("../resources/pieces/b_rook.png").scaled(20, 20),
          QPixmap("../resources/pieces/w_bishop.png").scaled(20, 20),
          QPixmap("../resources/pieces/w_king.png").scaled(20, 20),
          QPixmap("../resources/pieces/w_knight.png").scaled(20, 20),
          QPixmap("../resources/pieces/w_pawn.png.png").scaled(20, 20),
          QPixmap("../resources/pieces/w_queen.png").scaled(20, 20),
          QPixmap("../resources/pieces/w_rook.png").scaled(20, 20)]

        self.coil_width = 100
        self.coil_height = 40

        self.head_layout = QGridLayout()
        self.head_layout.setContentsMargins(0, 0, 0, 0)
        self.head_layout.setSpacing(0)
        self.head_layout.setAlignment(Qt.AlignCenter)

        self.head_widget = QWidget()
        self.head_widget.setLayout(self.head_layout)

        self.moves_table_layout = QGridLayout()
        self.moves_table_layout.setContentsMargins(0, 0, 0, 0)
        self.moves_table_layout.setSpacing(0)
        self.moves_table_layout.setAlignment(Qt.AlignTop)

        self.content_widget = QWidget()
        self.content_widget.setLayout(self.moves_table_layout)

        self.content_area = QScrollArea()
        self.content_area.setFixedSize(1200, 200)
        self.content_area.setWidget(self.content_widget)

        self.fill_layout = QVBoxLayout()
        self.fill_layout.setContentsMargins(0, 0, 0, 0)
        self.fill_layout.setSpacing(0)
        self.fill_layout.addWidget(self.head_widget)
        self.fill_layout.addWidget(self.content_area)

        self.create_header(col_am)
        self.create_content_rows(col_am, rA)

        self.moves_widget = QWidget()
        self.moves_widget.setLayout(self.fill_layout)

        self.setWidget(self.moves_widget)
        self.setStyleSheet(f"""
            QScrollArea {{
                border: none;            
            }}
        
            QScrollBar:horizontal, QScrollBar:vertical {{
                background-color: {color_theme[1]};
                color: {color_theme[3]};
                border: 1px solid {color_theme[3]}
            }}
            
            QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
                border: none;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
            }}
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
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
        points_header = QLabel("Przewaga")
        points_header.setFixedSize(150, 30)
        points_header.setAlignment(Qt.AlignCenter)
        points_header.setStyleSheet(header_styles)
        self.head_layout.addWidget(points_header, 0, 0)

        divider = math.ceil((self.size().width() - 150) / column_amount)
        for column in range(1, column_amount + 1):
            move_header = QLabel(str(column))
            if divider < self.coil_width:
                move_header.setFixedSize(self.coil_width, 30)
            else:
                move_header.setFixedSize(divider, 30)
            move_header.setAlignment(Qt.AlignCenter)
            move_header.setStyleSheet(header_styles)
            self.head_layout.addWidget(move_header, 0, column)

    def create_content_rows(self, column_amount, rows_amount):
        divider = math.ceil((self.size().width() - 150) / column_amount)
        for row in range(0, rows_amount):
            for column in range(0, column_amount + 1):
                coils_style = f'''
                    color: {color_theme[3]};
                    font-size: 18px;
                    border-bottom: 1px solid {color_theme[3]};
                '''
                if column % 2 == 0:
                    coils_style += f'''
                        background-color: {color_theme[1]};
                    '''
                else:
                    coils_style += f'''
                        background-color: {color_theme[0]};
                    '''
                move_coil = QWidget()
                move_lay = QHBoxLayout()
                move_lay.setContentsMargins(0, 0, 0, 0)
                move_lay.setSpacing(0)
                y = QLabel(moves[column])

                if column == 0:
                    move_coil.setFixedSize(150, self.coil_height)
                    y.setAlignment(Qt.AlignCenter)
                else:
                    if divider < self.coil_width:
                        move_coil.setFixedSize(self.coil_width, self.coil_height)
                    else:
                        move_coil.setFixedSize(divider, self.coil_height)
                    x = QLabel()
                    x.setPixmap(self.pieces[6])
                    x.setAlignment(Qt.AlignCenter)
                    move_lay.addWidget(x)
                move_lay.addWidget(y)
                move_coil.setLayout(move_lay)
                move_coil.setStyleSheet(coils_style)
                self.moves_table_layout.addWidget(move_coil, row, column)

    def update_size(self, new_size):
        self.setGeometry(0, (new_size.height() - 820) + 600, (new_size.width() - 1200) + 1200, 220)
        self.resize_elements(col_am, rA)

    def resize_elements(self, column_amount, row_amount):
        divider = math.floor((self.size().width() - 150) / column_amount)
        if divider < self.coil_width:
            self.moves_widget.setFixedSize((column_amount * self.coil_width) + 150, 200)
            self.head_widget.setFixedSize((column_amount * self.coil_width) + 150, 30)
            self.content_area.setFixedSize((column_amount * self.coil_width) + 150, 190)
            self.content_widget.setFixedSize((column_amount * self.coil_width) + 150, self.coil_height * row_amount)
            for column in range(1, column_amount):
                self.head_layout.itemAtPosition(0, column).widget().setFixedSize(self.coil_width, 30)
                for row in range(0, row_amount):
                    self.moves_table_layout.itemAtPosition(row, column).widget().setFixedSize(self.coil_width, self.coil_height)
        else:
            self.moves_widget.setFixedSize(divider * column_amount + 150, 200)
            self.head_widget.setFixedSize(divider * column_amount + 150, 30)
            self.content_area.setFixedSize(divider * column_amount + 155, 190)
            self.content_widget.setFixedSize(divider * column_amount + 150,  self.coil_height * row_amount)
            for column in range(1, column_amount):
                self.head_layout.itemAtPosition(0, column).widget().setFixedSize(divider, 30)
                for row in range(0, row_amount):
                    self.moves_table_layout.itemAtPosition(row, column).widget().setFixedSize(divider, self.coil_height)
