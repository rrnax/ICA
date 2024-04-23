from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QTextEdit, QSizePolicy, QApplication, QFileDialog
from PyQt5.QtCore import Qt
from sheard_memory import SharedMemoryStorage
from message_dialog import MessageDialog

class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()

        # Items
        self.close_btn = QPushButton("X", self)
        self.dialog_title = QLabel("Zapisz partię")
        self.bar_space = QWidget()
        self.close_bar = QWidget()
        self.content_widget = QWidget()
        self.fen_label = QLabel("FEN")
        self.fen_value = QTextEdit()
        self.fen_btn_widget = QWidget()
        self.fen_copy = QPushButton("Skopiuj")
        self.fen_save_in = QPushButton("Zapisz jako...")
        self.pgn_label = QLabel("PGN")
        self.pgn_value = QTextEdit()
        self.pgn_btn_widget = QWidget()
        self.pgn_copy = QPushButton("Skopiuj")
        self.pgn_save_in = QPushButton("Zapisz jako...")

        # Creating container
        self.set_items_properties()
        self.set_layouts()
        self.set_general_properties()
        self.save_style = self.create_style()
        self.setStyleSheet(self.save_style)
        self.assign_actions()

    def assign_actions(self):
        self.close_btn.clicked.connect(self.close)
        self.fen_copy.clicked.connect(self.copy_fen)
        self.pgn_copy.clicked.connect(self.copy_pgn)
        self.fen_save_in.clicked.connect(self.save_fen_in_file)
        self.pgn_save_in.clicked.connect(self.save_pgn_in_file)

    def set_general_properties(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("save-dialog")
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
        fen_btn_layout.addWidget(self.fen_copy)
        fen_btn_layout.addWidget(self.fen_save_in)
        self.fen_btn_widget.setLayout(fen_btn_layout)

        # Pgn buttons
        pgn_btn_layout = QHBoxLayout()
        pgn_btn_layout.setAlignment(Qt.AlignCenter)
        pgn_btn_layout.setSpacing(40)
        pgn_btn_layout.addWidget(self.pgn_copy)
        pgn_btn_layout.addWidget(self.pgn_save_in)
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
        self.close_btn.setObjectName("saves-close")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setFixedSize(30, 30)

        # Top bar
        self.bar_space.setFixedSize(760, 40)
        self.close_bar.setFixedSize(800, 40)
        self.close_bar.setObjectName("save-title")

        # Fen area
        self.fen_value.setMaximumHeight(40)
        self.fen_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.fen_value.setLineWrapMode(QTextEdit.NoWrap)
        self.fen_value.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.fen_value.setReadOnly(True)
        self.fen_value.setObjectName("save-fen-area")

        # Pgn area
        self.pgn_value.setFixedHeight(300)
        self.pgn_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pgn_value.setReadOnly(True)
        self.pgn_value.setObjectName("save-pgn-area")

        # Buttons
        self.fen_save_in.setCursor(Qt.PointingHandCursor)
        self.fen_save_in.setObjectName("fen-save")
        self.fen_copy.setCursor(Qt.PointingHandCursor)
        self.fen_copy.setObjectName("fen-copy")
        self.pgn_save_in.setCursor(Qt.PointingHandCursor)
        self.pgn_save_in.setObjectName("pgn-save")
        self.pgn_copy.setCursor(Qt.PointingHandCursor)
        self.pgn_copy.setObjectName("pgn-copy")

    def update_style(self):
        style = self.create_style()
        self.setStyleSheet(style)

    def create_style(self):
        return f"""
            #save-dialog {{
                background-color: {self.storage.color_theme[0]};
                border: 1px solid {self.storage.color_theme[3]}; 
            }}

            #saves-close {{
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
                font-size: 20px;
                border: none;
            }}

            #saves-close:hover {{
                background-color: red;
                color: {self.storage.color_theme[0]};
                border: 5px solid red;
                border-radius: 10px;
            }}

            #save-title {{
                border-bottom: 1px solid {self.storage.color_theme[3]};
            }}

            QLabel {{
                color: {self.storage.color_theme[3]};
                font-size: 18px;
            }}

            #save-fen-area, #save-pgn-area {{
                background-color: {self.storage.color_theme[1]};
                font-size: 20px;
                color: {self.storage.color_theme[3]};
                border: 1px solid {self.storage.color_theme[3]}; 
            }}
            
            QScrollBar:horizontal {{
                height: 10px;
                background-color: {self.storage.color_theme[1]};
                color: {self.storage.color_theme[3]};
                border: 1px solid {self.storage.color_theme[3]}
            }}
            
            QScrollBar:vertical {{
                width: 10px;
                background-color: {self.storage.color_theme[1]};
                color: {self.storage.color_theme[3]};
                border: 1px solid {self.storage.color_theme[3]}
            }}
            
            QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
                border: none;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
            }}
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {{
                background: {self.storage.color_theme[3]};
                border: none;
            }}
            
            #fen-save, #fen-copy, #pgn-save, #pgn-copy {{
                width: 150px;
                height: 30px;
                background-color: {self.storage.color_theme[3]};
                color: {self.storage.color_theme[0]};
                font-size: 20px;
                border: 1px solid {self.storage.color_theme[3]};
                border-radius: 5px;
            }}

            #fen-save:hover, #fen-copy:hover, #pgn-save:hover, #pgn-copy:hover {{
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
            }}
        """

    def load_fen(self, actual_FEN):
        self.fen_value.clear()
        self.fen_value.append(actual_FEN)

    def load_pgn(self, actual_PGN):
        self.pgn_value.clear()
        self.pgn_value.append(str(actual_PGN) + "\n\n")

    def copy_fen(self):
        clip_board = QApplication.clipboard()
        clip_board.clear(mode=clip_board.Clipboard)
        clip_board.setText(self.fen_value.toPlainText(), mode=clip_board.Clipboard)
        msg_label = QLabel("Skopiowano")
        msg_label.setStyleSheet(f"color: {self.storage.color_theme[3]};")
        info_msg = MessageDialog(content=msg_label)
        info_msg.exec()

    def copy_pgn(self):
        clip_board = QApplication.clipboard()
        clip_board.clear(mode=clip_board.Clipboard)
        clip_board.setText(self.pgn_value.toPlainText(), mode=clip_board.Clipboard)
        msg_label = QLabel("Skopiowano")
        msg_label.setStyleSheet(f"color: {self.storage.color_theme[3]};")
        info_msg = MessageDialog(content=msg_label)
        info_msg.exec()

    def save_fen_in_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz plik", "", "Pliki tekstowe (*.txt);;Wszystkie pliki (*)", options=options)
        if file_name:
            fen = self.fen_value.toPlainText()
            with open(file_name, "w") as file:
                file.write(fen)

    def save_pgn_in_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz plik", "", "Pliki Portable Game Notation (*.pgn);;Wszystkie pliki (*)", options=options)
        if file_name:
            pgn = self.pgn_value.toPlainText()
            with open(file_name, "w") as file:
                file.write(pgn)