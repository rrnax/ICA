import io

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QTextEdit, QSizePolicy,
                             QFileDialog)
from PyQt5.QtCore import Qt
from sheard_memory import SharedMemoryStorage
from chess import Board, pgn
from message_dialog import MessageDialog

class LoadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()

        # Items
        self.close_btn = QPushButton("X", self)
        self.dialog_title = QLabel("Wczytaj partię")
        self.bar_space = QWidget()
        self.close_bar = QWidget()
        self.content_widget = QWidget()
        self.fen_label = QLabel("FEN")
        self.fen_value = QTextEdit()
        self.fen_btn_widget = QWidget()
        self.fen_load_paste = QPushButton("Wczytaj wpisane")
        self.fen_load_file = QPushButton("Wczytaj z pliku")
        self.pgn_label = QLabel("PGN")
        self.pgn_value = QTextEdit()
        self.pgn_btn_widget = QWidget()
        self.pgn_load_paste = QPushButton("Wczytaj wpisane")
        self.pgn_load_file = QPushButton("Wczytaj z pliku")

        # Creating container
        self.set_items_properties()
        self.set_layouts()
        self.set_general_properties()
        self.save_style = self.create_style()
        self.setStyleSheet(self.save_style)
        self.assign_actions()

    def assign_actions(self):
        self.close_btn.clicked.connect(self.close)
        self.fen_load_paste.clicked.connect(self.load_paste_fen)
        self.pgn_load_paste.clicked.connect(self.load_paste_pgn)
        self.fen_load_file.clicked.connect(self.load_fen_from_file)
        self.pgn_load_file.clicked.connect(self.load_pgn_from_file)

    def set_general_properties(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("load-dialog")
        self.setFixedSize(800, 600)

    def set_layouts(self):
        # Dialog title
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.dialog_title)
        self.bar_space.setLayout(title_layout)

        # Top bar
        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignTop)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.addWidget(self.bar_space)
        bar_layout.addWidget(self.close_btn)
        self.close_bar.setLayout(bar_layout)

        # Fen buttons
        fen_btn_layout = QHBoxLayout()
        fen_btn_layout.setAlignment(Qt.AlignCenter)
        fen_btn_layout.setSpacing(40)
        fen_btn_layout.addWidget(self.fen_load_paste)
        fen_btn_layout.addWidget(self.fen_load_file)
        self.fen_btn_widget.setLayout(fen_btn_layout)

        # Pgn buttons
        pgn_btn_layout = QHBoxLayout()
        pgn_btn_layout.setAlignment(Qt.AlignCenter)
        pgn_btn_layout.setSpacing(40)
        pgn_btn_layout.addWidget(self.pgn_load_paste)
        pgn_btn_layout.addWidget(self.pgn_load_file)
        self.pgn_btn_widget.setLayout(pgn_btn_layout)

        # Content
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignVCenter)
        content_layout.setContentsMargins(40, 10, 40, 10)
        content_layout.addWidget(self.fen_label)
        content_layout.addWidget(self.fen_value)
        content_layout.addWidget(self.fen_btn_widget)
        content_layout.addWidget(self.pgn_label)
        content_layout.addWidget(self.pgn_value)
        content_layout.addWidget(self.pgn_btn_widget)
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
        self.close_btn.setObjectName("loads-close")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setFixedSize(30, 30)

        # Top bar
        self.bar_space.setFixedSize(760, 40)
        self.close_bar.setFixedSize(800, 40)
        self.close_bar.setObjectName("load-title")

        # Fen area
        self.fen_value.setMaximumHeight(40)
        self.fen_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.fen_value.setLineWrapMode(QTextEdit.NoWrap)
        self.fen_value.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.fen_value.setObjectName("load-fen-area")

        # Pgn area
        self.pgn_value.setFixedHeight(300)
        self.pgn_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pgn_value.setObjectName("load-pgn-area")

        # Buttons
        self.fen_load_file.setCursor(Qt.PointingHandCursor)
        self.fen_load_file.setObjectName("fen-load-file")
        self.fen_load_paste.setCursor(Qt.PointingHandCursor)
        self.fen_load_paste.setObjectName("fen-paste")
        self.pgn_load_file.setCursor(Qt.PointingHandCursor)
        self.pgn_load_file.setObjectName("pgn-load-file")
        self.pgn_load_paste.setCursor(Qt.PointingHandCursor)
        self.pgn_load_paste.setObjectName("pgn-paste")

        # Labels
        self.dialog_title.setStyleSheet(f"color: {self.storage.color_theme[3]};font-size: 18px;")
        self.fen_label.setStyleSheet(f"color: {self.storage.color_theme[3]};font-size: 18px;")
        self.pgn_label.setStyleSheet(f"color: {self.storage.color_theme[3]};font-size: 18px;")

    def create_style(self):
        return f"""
            #load-dialog {{
                background-color: {self.storage.color_theme[0]};
                border: 1px solid {self.storage.color_theme[3]}; 
            }}

            #loads-close {{
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
                font-size: 20px;
                border: none;
            }}

            #loads-close:hover {{
                background-color: red;
                color: {self.storage.color_theme[0]};
                border: 5px solid red;
                border-radius: 10px;
            }}

            #load-title {{
                border-bottom: 1px solid {self.storage.color_theme[3]};
            }}

            #load-fen-area, #load-pgn-area {{
                background-color: {self.storage.color_theme[1]};
                font-size: 20px;
                color: {self.storage.color_theme[3]};
                border: 1px solid {self.storage.color_theme[3]}; 
            }}

            #fen-load-file, #fen-paste, #pgn-load-file, #pgn-paste {{
                width: 200px;
                height: 30px;
                background-color: {self.storage.color_theme[3]};
                color: {self.storage.color_theme[0]};
                font-size: 20px;
                border: 1px solid {self.storage.color_theme[3]};
                border-radius: 5px;
            }}

            #fen-load-file:hover, #fen-paste:hover, #pgn-load-file:hover, #pgn-paste:hover {{
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
            }}
        """

    def load_fen_from_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik", "",
                                                   "Wszystkie pliki (*);;Tekstowe pliki (*.txt)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                try:
                    fen = file.readline()
                    check_board = Board()
                    check_board.set_fen(fen)
                except ValueError as error:
                    msg_label = QLabel("Nieprawidłowy FEN")
                    msg_label.setStyleSheet(f"color: {self.storage.color_theme[3]};")
                    error_msg = MessageDialog(msg_label)
                    error_msg.exec()
                else:
                    self.parent().load_board("fen", fen)
                    self.close()
                    self.parent().close_menu()

    def load_paste_fen(self):
        try:
            fen = self.fen_value.toPlainText()
            check_board = Board()
            check_board.set_fen(fen)
        except ValueError as error:
            msg_label = QLabel("Nieprawidłowy FEN")
            msg_label.setStyleSheet(f"color: {self.storage.color_theme[3]};")
            error_msg = MessageDialog(content=msg_label)
            error_msg.exec()
        else:
            self.parent().load_board("fen", fen)
            self.close()
            self.parent().close_menu()

    def load_pgn_from_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik", "",
                                                   "Pliki Portaable Game Notation (*.pgn);;Tekstowe pliki (*.txt)", options=options)
        if file_name:
            with open(file_name) as file:
                game = pgn.read_game(file)
                if game is not None:
                    self.close()
                    self.parent().close_menu()
                    self.parent().load_board("pgn", game)
                else:
                    msg_label = QLabel("Nieprawidłowy PGN")
                    msg_label.setStyleSheet(f"color: {self.storage.color_theme[3]};")
                    error_msg = MessageDialog(msg_label)
                    error_msg.exec()

    def load_paste_pgn(self):
        pgn_str = self.pgn_value.toPlainText()
        string_io = io.StringIO(pgn_str)
        game = pgn.read_game(string_io)
        if game is not None:
            self.close()
            self.parent().close_menu()
            self.parent().load_board("pgn", game)
        else:
            msg_label = QLabel("Nieprawidłowy PGN")
            msg_label.setStyleSheet(f"color: {self.storage.color_theme[3]};")
            error_msg = MessageDialog(content=msg_label)
            error_msg.exec()
