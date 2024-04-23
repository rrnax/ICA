from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from sheard_memory import SharedMemoryStorage


class PromotionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()
        self.pieces_color = "white"

        # Items
        self.close_btn = QPushButton("X", self)
        self.dialog_title = QLabel("Wybierz figurę do promocji")
        self.bar_space = QWidget()
        self.close_bar = QWidget()
        self.content_widget = QWidget()
        self.queen = QPushButton()
        self.rook = QPushButton()
        self.bishop = QPushButton()
        self.knight = QPushButton()

        # Creating container
        self.set_items_properties()
        self.set_layouts()
        self.set_general_properties()
        self.save_style = self.create_style()
        self.setStyleSheet(self.save_style)
        self.assign_actions()

    def assign_actions(self):
        self.close_btn.clicked.connect(self.close)
        self.queen.clicked.connect(self.send_queen)
        self.rook.clicked.connect(self.send_rook)
        self.bishop.clicked.connect(self.send_bishop)
        self.knight.clicked.connect(self.send_knight)

    def set_general_properties(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("promotion-dialog")
        self.setFixedSize(500, 160)

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
        content_layout = QHBoxLayout()
        content_layout.setAlignment(Qt.AlignHCenter)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        content_layout.addWidget(self.queen)
        content_layout.addWidget(self.bishop)
        content_layout.addWidget(self.rook)
        content_layout.addWidget(self.knight)
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
        self.close_btn.setObjectName("promotion-close")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setFixedSize(30, 30)

        # Buttons
        self.queen.setFixedSize(100, 100)
        self.queen.setCursor(Qt.PointingHandCursor)
        self.bishop.setFixedSize(100, 100)
        self.bishop.setCursor(Qt.PointingHandCursor)
        self.rook.setFixedSize(100, 100)
        self.rook.setCursor(Qt.PointingHandCursor)
        self.knight.setFixedSize(100, 100)
        self.knight.setCursor(Qt.PointingHandCursor)
        self.queen.setObjectName("queen_btn")
        self.bishop.setObjectName("bishop_btn")
        self.rook.setObjectName("rook_btn")
        self.knight.setObjectName("knight_btn")

        # Labels
        self.dialog_title.setStyleSheet(f"color: {self.storage.color_theme[3]};font-size: 18px;")

    def set_pieces_color(self, color):
        self.pieces_color = color
        pieces = {
            "b": QPixmap("../resources/pieces/b_bishop.png"),
            "n": QPixmap("../resources/pieces/b_knight.png"),
            "q": QPixmap("../resources/pieces/b_queen.png"),
            "r": QPixmap("../resources/pieces/b_rook.png"),
            "B": QPixmap("../resources/pieces/w_bishop.png"),
            "N": QPixmap("../resources/pieces/w_knight.png"),
            "Q": QPixmap("../resources/pieces/w_queen.png"),
            "R": QPixmap("../resources/pieces/w_rook.png")
        }
        if self.pieces_color == "white":
            self.queen.setIcon(QIcon(pieces['Q']))
            self.bishop.setIcon(QIcon(pieces['B']))
            self.rook.setIcon(QIcon(pieces['R']))
            self.knight.setIcon(QIcon(pieces['N']))
        else:
            self.queen.setIcon(QIcon(pieces['q']))
            self.bishop.setIcon(QIcon(pieces['b']))
            self.rook.setIcon(QIcon(pieces['r']))
            self.knight.setIcon(QIcon(pieces['n']))
        self.queen.setIconSize(QSize(80, 80))
        self.rook.setIconSize(QSize(80, 80))
        self.bishop.setIconSize(QSize(80, 80))
        self.knight.setIconSize(QSize(80, 80))

    def update_style(self):
        style = self.create_style()
        self.setStyleSheet(style)

    def send_rook(self):
        if self.pieces_color == "white":
            self.parent().set_promoted_info(["../resources/pieces/w_rook.png", "R"])
        else:
            self.parent().set_promoted_info(["../resources/pieces/b_rook.png", "r"])
        self.close()

    def send_queen(self):
        if self.pieces_color == "white":
            self.parent().set_promoted_info(["../resources/pieces/w_queen.png", "Q"])
        else:
            self.parent().set_promoted_info(["../resources/pieces/b_queen.png", "q"])
        self.close()

    def send_bishop(self):
        if self.pieces_color == "white":
            self.parent().set_promoted_info(["../resources/pieces/w_bishop.png", "B"])
        else:
            self.parent().set_promoted_info(["../resources/pieces/b_bishop.png", "b"])
        self.close()

    def send_knight(self):
        if self.pieces_color == "white":
            self.parent().set_promoted_info(["../resources/pieces/w_knight.png", "N"])
        else:
            self.parent().set_promoted_info(["../resources/pieces/b_knight.png", "n"])
        self.close()

    def create_style(self):
        return f"""
               #promotion-dialog {{
                   background-color: {self.storage.color_theme[0]};
                   border: 1px solid {self.storage.color_theme[3]}; 
               }}

               #promotion-close {{
                   background-color: {self.storage.color_theme[0]};
                   color: {self.storage.color_theme[3]};
                   font-size: 20px;
                   border: none;
               }}

               #promotion-close:hover {{
                   background-color: red;
                   color: {self.storage.color_theme[0]};
                   border: 5px solid red;
                   border-radius: 10px;
               }}
               
               #queen_btn, #bishop_btn, #rook_btn, #knight_btn {{
                    background-color: {self.storage.color_theme[0]};
                    border: none;
               }}
            
               #queen_btn:hover, #bishop_btn:hover, #rook_btn:hover, #knight_btn:hover {{ 
                    background-color: {self.storage.color_theme[3]};
                    border-radius: 10px;
               }}
        """