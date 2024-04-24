import math
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from engine import ChessEngine
from sheard_memory import SharedMemoryStorage
from loader import Loader


# Move option list widget is responsible for showing parsed data comes from engine and correct displaying it.
# It's important to be careful with change dynamic struct and calc of data containers.
# Dynamic containers used here are located in SharedMemoryStorage singleton class
class OptionalMovesList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()
        self.engine = ChessEngine()
        self.coil_width = 100
        self.coil_height = 50
        self.actual_column_amount = None
        self.actual_row_amount = None
        self.pieces = self.set_images_dict()

        # Items
        self.loader = Loader("../resources/duck.gif")
        self.head_widget = QWidget()
        self.content_widget = QWidget()
        self.content_area = QScrollArea()
        self.moves_widget = QWidget()

        # layouts
        self.head_layout = QGridLayout()
        self.moves_table_layout = QGridLayout()
        self.fill_layout = QVBoxLayout()

        # Create operations
        self.set_general_properties()
        self.set_items_properties()
        self.set_layouts()

        self.head_widget.hide()
        self.content_area.hide()

        self.setWidget(self.moves_widget)

    def set_layouts(self):
        # Header layout
        self.head_layout.setContentsMargins(0, 0, 0, 0)
        self.head_layout.setSpacing(0)
        self.head_layout.setAlignment(Qt.AlignCenter)

        for index, element in enumerate(self.storage.head_labels):
            self.head_layout.addWidget(element, 0, index)

        self.head_widget.setLayout(self.head_layout)

        # Move options layout
        self.moves_table_layout.setContentsMargins(0, 0, 0, 0)
        self.moves_table_layout.setSpacing(0)
        self.moves_table_layout.setAlignment(Qt.AlignTop)

        for i, item_row in enumerate(self.storage.content_rows):
            for j, item_column in enumerate(self.storage.content_rows[i]):
                self.moves_table_layout.addWidget(item_column, i, j)

        self.content_widget.setLayout(self.moves_table_layout)

        # General layout
        self.fill_layout.setContentsMargins(0, 0, 0, 0)
        self.fill_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)
        self.fill_layout.setSpacing(0)
        self.fill_layout.addWidget(self.loader)
        self.fill_layout.addWidget(self.head_widget)
        self.fill_layout.addWidget(self.content_area)
        self.moves_widget.setLayout(self.fill_layout)

    def set_general_properties(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("main-scroll")

    def set_items_properties(self):
        # Loader
        self.loader.setObjectName("loader")
        self.loader.start_animation()

        # Content
        self.content_area.setFixedHeight(190)
        self.content_area.setWidget(self.content_widget)
        self.content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # General
        self.moves_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_header(self, column_amount):
        # Calculate size of moves header
        try:
            self.hide_headers()
            header_width = None
            header_height = 30
            column_width = None
            divider = math.ceil((self.size().width() - 150) / column_amount)

            if divider < self.coil_width:
                header_width = 150 + self.coil_width * column_amount
                column_width = self.coil_width
            else:
                header_width = 150 + divider * column_amount
                column_width = divider

        except Exception as er:
            self.hide_headers()
            self.hide_content()
            self.loader.show()
            self.storage.logger.debug(er)
            self.storage.logger.exception("Błąd: ")

        # Set sizes if calculation pass through
        else:
            self.head_widget.setFixedSize(header_width, header_height)

            self.storage.head_labels[0].setText("Przewaga")
            self.storage.head_labels[0].setFixedSize(150, header_height)
            self.storage.head_labels[0].show()

            for column in range(1, column_amount + 1):
                self.storage.head_labels[column].setText(str(column))
                self.storage.head_labels[column].setFixedSize(column_width, header_height)
                self.storage.head_labels[column].show()

    def resize_header(self, column_amount):
        # Recalculate sizes
        try:
            header_width = None
            header_height = 30
            column_width = None
            divider = math.ceil((self.size().width() - 150) / column_amount)

            if divider < self.coil_width:
                header_width = 150 + self.coil_width * column_amount
                column_width = self.coil_width
            else:
                header_width = 150 + divider * column_amount
                column_width = divider

        except Exception as er:
            self.hide_headers()
            self.hide_content()
            self.loader.show()
            self.storage.logger.debug(er)
            self.storage.logger.exception("Błąd: ")
        # Join sizes to reality
        else:
            self.head_widget.setFixedSize(header_width, header_height)
            print("XD")

            for column in range(1, column_amount + 1):
                self.storage.head_labels[column].setFixedSize(column_width, header_height)

    def create_content_rows(self, column_amount, rows_amount, list_of_lists):
        # Calculate content sizes
        try:
            self.hide_content()
            content_width = None
            content_height = rows_amount * self.coil_height
            column_width = None
            divider = math.ceil((self.size().width() - 150) / column_amount)

            if divider < self.coil_width:
                content_width = 150 + self.coil_width * column_amount
                column_width = self.coil_width
            else:
                content_width = 150 + divider * column_amount
                column_width = divider

        except Exception as er:
            self.hide_headers()
            self.hide_content()
            self.loader.show()
            self.storage.logger.debug(er)
            self.storage.logger.exception("Błąd: ")

        # Create content with correct sizes
        else:
            self.content_widget.setFixedSize(content_width, content_height)

            for row in range(0, rows_amount):

                self.storage.content_rows[row][0].layout().itemAt(0).widget().setText(str(list_of_lists[row][0]))
                self.storage.content_rows[row][0].setFixedSize(150, self.coil_height)
                self.storage.content_rows[row][0].show()

                for column in range(1, column_amount + 1):

                    self.storage.content_rows[row][column].setFixedSize(column_width, self.coil_height)

                    if column < len(list_of_lists[row]):
                        (self.storage.content_rows[row][column].layout().itemAt(0).widget()
                         .setPixmap(self.pieces[self.engine.pieces_ids_list[row][column]]))
                    else:
                        self.storage.content_rows[row][column].layout().itemAt(0).widget().setText(" ")

                    if column < len(list_of_lists[row]):
                        self.storage.content_rows[row][column].layout().itemAt(1).widget().setText(
                            str(list_of_lists[row][column]))
                    else:
                        self.storage.content_rows[row][column].layout().itemAt(1).widget().setText(" ")

                    self.storage.content_rows[row][column].show()

    def resize_content(self, column_amount, rows_amount):
        # Calculate resizes
        try:
            content_width = None
            content_height = rows_amount * self.coil_height
            column_width = None
            divider = math.ceil((self.size().width() - 150) / column_amount)

            if divider < self.coil_width:
                content_width = 150 + self.coil_width * column_amount
                column_width = self.coil_width
            else:
                content_width = 150 + divider * column_amount
                column_width = divider

        except Exception as er:
            self.hide_headers()
            self.hide_content()
            self.loader.show()
            self.storage.logger.debug(er)
            self.storage.logger.exception("Błąd: ")

        # Update in reality
        else:
            self.content_widget.setFixedSize(content_width, content_height)
            for row in range(0, rows_amount):
                for column in range(1, column_amount + 1):
                    self.storage.content_rows[row][column].setFixedSize(column_width, self.coil_height)

    def update_size(self, new_size):
        self.setGeometry(0, (new_size.height() - 820) + 600, (new_size.width() - 1200) + 1200, 220)
        self.resize_header(self.actual_column_amount)
        self.resize_content(self.actual_column_amount, self.actual_row_amount)

    def show_loader(self):
        self.loader.show()
        self.loader.start_animation()

    def hide_loader(self):
        self.loader.stop_animation()
        self.loader.hide()

    # Creating table with optional moves
    def set_move_table(self, option_list):
        # Check correct
        try:
            column_amount = 0
            row_amount = len(option_list)
            for list_id in option_list:
                if len(list_id) > column_amount:
                    column_amount = len(list_id)

        except Exception as er:
            self.storage.logger.debug(er)
            self.storage.logger.exception("Błąd: ")
        else:
            self.actual_column_amount = column_amount
            self.actual_row_amount = row_amount
            self.create_header(column_amount)
            self.create_content_rows(column_amount, row_amount, option_list)

    def hide_headers(self):
        for element in self.storage.head_labels:
            element.hide()

    def hide_content(self):
        for i, item_row in enumerate(self.storage.content_rows):
            for j, item_column in enumerate(self.storage.content_rows[i]):
                item_column.hide()

    def update_theme(self):
        self.storage.update_options_list()
        self.loader.update_style()

    def set_images_dict(self):
        return {
            "b": QPixmap("../resources/pieces/b_bishop.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "k": QPixmap("../resources/pieces/b_king.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "n": QPixmap("../resources/pieces/b_knight.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "p": QPixmap("../resources/pieces/b_pawn.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "q": QPixmap("../resources/pieces/b_queen.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "r": QPixmap("../resources/pieces/b_rook.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "B": QPixmap("../resources/pieces/w_bishop.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "K": QPixmap("../resources/pieces/w_king.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "N": QPixmap("../resources/pieces/w_knight.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "P": QPixmap("../resources/pieces/w_pawn.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "Q": QPixmap("../resources/pieces/w_queen.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "R": QPixmap("../resources/pieces/w_rook.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        }


