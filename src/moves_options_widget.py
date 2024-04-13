from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import math
from loader import Loader
from sheard_memory import SharedMemoryStorage

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]
col_am = 20
moves = ["+1,922", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2",
         "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2",
         "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2", "a1b2"]
rA = 4


class MovesOptionsList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()

        self.pieces = [
            QPixmap("../resources/pieces/b_bishop.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/b_king.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/b_knight.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/b_pawn.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/b_queen.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/b_rook.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/w_bishop.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/w_king.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/w_knight.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/w_pawn.png.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/w_queen.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap("../resources/pieces/w_rook.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)]

        self.coil_width = 100
        self.coil_height = 50

        self.points_header = QLabel()

        self.head_layout = QGridLayout()
        self.head_layout.setContentsMargins(0, 0, 0, 0)
        self.head_layout.setSizeConstraint(QGridLayout.SetMinAndMaxSize)
        self.head_layout.setSpacing(0)
        self.head_layout.setAlignment(Qt.AlignCenter)

        self.head_widget = QWidget()
        self.head_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.head_widget.setLayout(self.head_layout)

        self.moves_table_layout = QGridLayout()
        self.moves_table_layout.setContentsMargins(0, 0, 0, 0)
        self.moves_table_layout.setSizeConstraint(QGridLayout.SetMinAndMaxSize)
        self.moves_table_layout.setSpacing(0)
        self.moves_table_layout.setAlignment(Qt.AlignTop)

        self.loader = Loader("../resources/pika.gif")
        self.loader.setObjectName("loader")
        self.loader.start_animation()

        self.content_widget = QWidget()
        self.content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_widget.setLayout(self.moves_table_layout)

        self.content_area = QScrollArea()
        self.content_area.setFixedHeight(173)
        # self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content_area.setWidget(self.content_widget)

        self.fill_layout = QVBoxLayout()
        self.fill_layout.setContentsMargins(0, 0, 0, 0)
        self.fill_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        self.fill_layout.setSpacing(0)
        self.fill_layout.addWidget(self.loader)
        self.fill_layout.addWidget(self.head_widget)
        self.fill_layout.addWidget(self.content_area)

        self.moves_widget = QWidget()
        self.moves_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.moves_widget.setLayout(self.fill_layout)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignCenter)
        self.setWidget(self.moves_widget)
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: {color_theme[1]};
                color: {color_theme[3]};
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
            
            #loader {{
                background-color: {color_theme[1]};
            }}
        """)

    def create_header(self, column_amount):
        self.storage.head_labels[0].setText("Przewaga")
        self.storage.head_labels[0].setFixedSize(150, 30)

        self.storage.head_labels[0].setAlignment(Qt.AlignCenter)
        self.head_layout.addWidget(self.storage.head_labels[0], 0, 0)

        divider = math.ceil((self.size().width() - 150) / column_amount)
        for column in range(1, column_amount + 1):
            self.storage.head_labels[column].setText(str(column))
            self.storage.head_labels[column].setAlignment(Qt.AlignCenter)
            if divider < self.coil_width:
                self.storage.head_labels[column].setFixedSize(self.coil_width, 30)
            else:
                self.storage.head_labels[column].setFixedSize(divider, 30)
            self.head_layout.addWidget(self.storage.head_labels[column], 0, column)

    def create_content_rows(self, column_amount, rows_amount, list_of_lists):
        divider = math.ceil((self.size().width() - 150) / column_amount)

        for row in range(0, rows_amount):

            for column in range(0, column_amount + 1):
                self.storage.content_rows[row][column].setContentsMargins(0, 0, 0, 0)
                self.storage.content_rows[row][column].layout().setSpacing(0)

                if column == 0:
                    self.storage.content_rows[row][column].layout().itemAt(0).widget().setText(
                        str(list_of_lists[row][column]))
                    self.storage.content_rows[row][column].setFixedSize(150, self.coil_height)
                    self.storage.content_rows[row][column].layout().itemAt(0).widget().setAlignment(Qt.AlignCenter)
                else:
                    if column < len(list_of_lists[row]):
                        self.storage.content_rows[row][column].layout().itemAt(1).widget().setText(
                            str(list_of_lists[row][column]))
                    else:
                        self.storage.content_rows[row][column].layout().itemAt(1).widget().setText(" ")

                    if divider < self.coil_width:
                        self.storage.content_rows[row][column].setFixedSize(self.coil_width, self.coil_height)
                    else:
                        self.storage.content_rows[row][column].setFixedSize(divider, self.coil_height)

                    if column < len(list_of_lists[row]):
                        self.storage.content_rows[row][column].layout().itemAt(0).widget().setPixmap(self.pieces[6])
                    else:
                        self.storage.content_rows[row][column].layout().itemAt(0).widget().setText(" ")
                    self.storage.content_rows[row][column].layout().itemAt(0).widget().setAlignment(Qt.AlignCenter)

                self.moves_table_layout.addWidget(self.storage.content_rows[row][column], row, column)

    def update_size(self, new_size):
        self.setGeometry(0, (new_size.height() - 820) + 600, (new_size.width() - 1200) + 1200, 220)
        # if self.check_fill_layout():
        #     self.resize_elements(col_am, rA)

    def resize_elements(self, column_amount, row_amount):
        divider = math.floor((self.size().width() - 150) / column_amount)
        if divider < self.coil_width:
            self.moves_widget.setFixedSize((column_amount * self.coil_width) + 150, 203)
            self.head_widget.setFixedSize((column_amount * self.coil_width) + 150, 30)
            self.content_area.setFixedSize((column_amount * self.coil_width) + 150, 190)
            self.content_widget.setFixedSize((column_amount * self.coil_width) + 150, self.coil_height * row_amount)
            for column in range(1, column_amount):
                self.head_layout.itemAtPosition(0, column).widget().setFixedSize(self.coil_width, 30)
                for row in range(0, row_amount):
                    self.moves_table_layout.itemAtPosition(row, column).widget().setFixedSize(self.coil_width,
                                                                                              self.coil_height)
        else:
            self.moves_widget.setFixedSize(divider * column_amount + 150, 200)
            self.head_widget.setFixedSize(divider * column_amount + 150, 30)
            self.content_area.setFixedSize(divider * column_amount + 155, 190)
            self.content_widget.setFixedSize(divider * column_amount + 150, self.coil_height * row_amount)
            for column in range(1, column_amount):
                self.head_layout.itemAtPosition(0, column).widget().setFixedSize(divider, 30)
                for row in range(0, row_amount):
                    self.moves_table_layout.itemAtPosition(row, column).widget().setFixedSize(divider, self.coil_height)

    def show_loader(self):
        self.loader.show()
        self.loader.start_animation()

    def hide_loader(self):
        self.loader.stop_animation()
        self.loader.hide()

    def set_move_table(self, option_list):
        column_amount = 0
        row_amount = len(option_list)
        for list_id in option_list:
            if len(list_id) > column_amount:
                column_amount = len(list_id)

        self.create_header(column_amount)
        self.create_content_rows(column_amount, row_amount, option_list)

