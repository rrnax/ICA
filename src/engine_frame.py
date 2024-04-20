from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QPushButton, QMenu
from PyQt5.QtGui import QCursor, QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QSize
from settings_dialog import SettingsDialog
from engine import ChessEngine
from sheard_memory import SharedMemoryStorage


class EngineFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = ChessEngine()
        self.storage = SharedMemoryStorage()

        # Nodes elements
        self.sort_menu = QMenu(self)
        self.sort_menu.addAction("Najlepsze czarne", self.better_black)
        self.sort_menu.addAction("Najlepsze białe", self.better_white)
        self.sort_menu.setCursor(QCursor(Qt.PointingHandCursor))

        self.engine_label = QLabel("Silnik:")
        self.depth_label = QLabel("Ilość ruchów do przodu:")
        self.elo_label = QLabel("Elo (FIDE):")

        self.moves_sort_button = QPushButton()
        self.engine_settings_button = QPushButton(self)
        self.left_widget = QWidget()
        self.right_widget = QWidget()

        self.set_items_properties()

        # Layouts parts
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(20, 0, 0, 0)
        left_layout.addWidget(self.engine_label)
        left_layout.addWidget(self.depth_label)
        left_layout.addWidget(self.elo_label)
        left_layout.setSpacing(85)

        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.moves_sort_button)
        right_layout.addWidget(self.engine_settings_button)

        self.left_widget.setLayout(left_layout)

        self.right_widget.setLayout(right_layout)

        # Layout
        self.engine_frame_layout = QHBoxLayout()
        self.engine_frame_layout.addWidget(self.left_widget)
        self.engine_frame_layout.addWidget(self.right_widget)
        self.engine_frame_layout.setContentsMargins(0, 0, 0, 0)

        # Frame
        self.setLayout(self.engine_frame_layout)
        self.setGeometry(0, 550, 1200, 50)
        self.setObjectName("engine-frame")
        self.engine_style = self.create_style()
        self.setStyleSheet(self.engine_style)

        self.engine_settings_button.clicked.connect(self.settings_up)
        
    def set_items_properties(self):
        # Sort button
        self.moves_sort_button.setFixedSize(40, 40)
        self.moves_sort_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.moves_sort_button.setIcon(QIcon('../resources/up-and-down-arrow.png'))
        self.moves_sort_button.setIconSize(QSize(30, 30))
        self.moves_sort_button.setMenu(self.sort_menu)
        self.moves_sort_button.setObjectName("sort-btn")

        # Engine button
        self.engine_settings_button.setFixedSize(40, 40)
        self.engine_settings_button.setObjectName("engine-settings")
        self.engine_settings_button.setIcon(QIcon('../resources/gear.png'))
        self.engine_settings_button.setIconSize(QSize(30, 30))
        self.engine_settings_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.engine_settings_button.setObjectName("engine-sets-btn")
        
        # Widgets
        self.left_widget.setStyleSheet(f"color: {self.storage.color_theme[3]}; font-size: 18px;")
        self.right_widget.setObjectName("right-widget")
        self.right_widget.setFixedSize(100, 48)

    def update_size(self, new_size):
        # self.engine_frame_layout.setSpacing(400 + new_size.width()-1200)
        self.setGeometry(0, (new_size.height() - 820) + 550, (new_size.width() - 1200) + 1200, 50)

    def settings_up(self):
        setting_window = SettingsDialog()
        setting_window.exec()

    def set_engine_label(self, text):
        self.engine_label.setText("Silnik: " + text)

    def set_depth_label(self, text):
        self.depth_label.setText("Ilość ruchów do przodu: " + text)

    def set_elo_label(self, text):
        self.elo_label.setText("Elo (FIDE): " + text)

    def update_values(self):
        self.set_engine_label(self.engine.engine_name)
        self.set_depth_label(str(self.engine.limits.depth))
        self.set_elo_label(str(self.engine.opponent.rating))

    def better_black(self):
        black_sorted_list = sorted(self.engine.last_result, key=lambda x: x[0].score())
        self.engine.last_result = black_sorted_list
        self.engine.pieces_ids_list = self.engine.find_pieces_ids()
        self.engine.moves_frame.set_move_table(self.engine.last_result)

    def better_white(self):
        white_sorted_list = sorted(self.engine.last_result, key=lambda x: x[0].score(), reverse=True)
        self.engine.last_result = white_sorted_list
        self.engine.pieces_ids_list = self.engine.find_pieces_ids()
        self.engine.moves_frame.set_move_table(self.engine.last_result)

    def update_theme(self):
        self.left_widget.setStyleSheet(f"color: {self.storage.color_theme[3]}; font-size: 18px;")
        style = self.create_style()
        self.setStyleSheet(style)
        
    def create_style(self):
        return f"""
            #engine-frame {{
                background-color: {self.storage.color_theme[1]};
                border-top: 1px solid {self.storage.color_theme[3]};
                border-bottom: 1px solid {self.storage.color_theme[3]};
            }}
                
            #right-widget {{
                background-color: {self.storage.color_theme[1]};
            }}
            
            #sort-btn, #engine-sets-btn {{
                border: none;
            }}
            
            #sort-btn::menu-indicator {{
                width: 0px;
            }}
            
            #sort-btn:hover, #engine-sets-btn:hover {{
                color: {self.storage.color_theme[0]};
                background-color: {self.storage.color_theme[3]};
                border: 1px solid {self.storage.color_theme[0]};
                border-radius: 10px;
            }}
            
            QMenu {{
                color: {self.storage.color_theme[3]};
                background-color: {self.storage.color_theme[1]};
                border: 1px solid {self.storage.color_theme[3]};
            }}
            
            QMenu::item {{
                padding: 5px 10px;
            }}
            
            QMenu::item:selected {{
                color: {self.storage.color_theme[0]};
                background-color: {self.storage.color_theme[1]};
            }}
        """

#<a href="https://www.flaticon.com/free-icons/menu-bar" title="menu bar icons">Menu bar icons created by Vector Squad - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/sort-ascending" title="sort ascending icons">Sort ascending icons created by Infinite Dendrogram - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/settings" title="settings icons">Settings icons created by Freepik - Flaticon</a>

