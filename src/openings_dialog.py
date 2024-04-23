from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QListWidget
from PyQt5.QtCore import Qt
from sheard_memory import SharedMemoryStorage
import io
from chess import pgn
from message_dialog import MessageDialog


class OpeningsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()

        # Items
        self.close_btn = QPushButton("X", self)
        self.dialog_title = QLabel("Otwarcia szachowe")
        self.bar_space = QWidget()
        self.close_bar = QWidget()
        self.content_widget = QWidget()
        self.openings_list_widget = QListWidget()

        # Creating container
        self.set_items_properties()
        self.set_layouts()
        self.set_general_properties()
        self.save_style = self.create_style()
        self.setStyleSheet(self.save_style)
        for item in self.storage.openings_widgets:
            self.openings_list_widget.addItem(item)

        self.assign_actions()

    def assign_actions(self):
        self.close_btn.clicked.connect(self.close)
        self.openings_list_widget.itemDoubleClicked.connect(self.chosed_item)

    def set_general_properties(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("openings-dialog")
        self.setFixedSize(500, 600)

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
        content_layout.setContentsMargins(20, 5, 20, 20)
        content_layout.addWidget(self.openings_list_widget)
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
        # self.close_bar.setObjectName("top-bar-opens")
        self.close_btn.setObjectName("openings-close")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setFixedSize(30, 30)

        # Labels
        self.dialog_title.setObjectName("openings-title")

        # List
        self.openings_list_widget.setSpacing(5)
        self.openings_list_widget.setObjectName("list-widget")

    def update_style(self):
        style = self.create_style()
        self.setStyleSheet(style)

    def chosed_item(self):
        actual_item = self.openings_list_widget.currentItem().text()
        pgn_str = self.storage.find_opening(actual_item)
        string_io = io.StringIO(pgn_str)
        game = pgn.read_game(string_io)
        if game is not None:
            self.close()
            self.parent().close_menu()
            self.parent().load_board("pgn", game)
        else:
            msg_label = QLabel("Błąd w otwarciu!")
            msg_label.setStyleSheet(f"color: {self.storage.color_theme[3]};")
            error_msg = MessageDialog(content=msg_label)
            error_msg.exec()


    def create_style(self):
        return f"""
               #openings-dialog {{
                   background-color: {self.storage.color_theme[0]};
                   border: 1px solid {self.storage.color_theme[3]}; 
               }}

               #openings-close {{
                   background-color: {self.storage.color_theme[0]};
                   color: {self.storage.color_theme[3]};
                   font-size: 20px;
                   border: none;
               }}
               
               #openings-title {{
                    color: {self.storage.color_theme[3]};
                    font-size: 18px;
               }}
                
               #top-bar-opens {{
                    border-bottom: 1px solid {self.storage.color_theme[3]};
               }}
               
               #list-widget {{
                   background-color: {self.storage.color_theme[1]};
                   color: {self.storage.color_theme[3]};
                   font-size: 20px;
                   border: 1px solid {self.storage.color_theme[3]};
               }}

               #openings-close:hover {{
                   background-color: red;
                   color: {self.storage.color_theme[0]};
                   border: 5px solid red;
                   border-radius: 10px;
               }}
        """