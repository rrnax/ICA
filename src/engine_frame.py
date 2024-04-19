from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QPushButton, QMenu
from PyQt5.QtGui import QCursor, QIcon, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QSize
from settings_dialog import SettingsDialog
from engine import ChessEngine
from sheard_memory import color_theme
#<a href="https://www.flaticon.com/free-icons/menu-bar" title="menu bar icons">Menu bar icons created by Vector Squad - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/sort-ascending" title="sort ascending icons">Sort ascending icons created by Infinite Dendrogram - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/settings" title="settings icons">Settings icons created by Freepik - Flaticon</a>


class EngineFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = ChessEngine()

        # Nodes elements
        sort_menu = QMenu(self)
        sort_menu.addAction("Najlepsze czarne", self.better_black)
        sort_menu.addAction("Najlepsze białe", self.better_white)
        sort_menu.setCursor(QCursor(Qt.PointingHandCursor))

        self.engine_label = QLabel("Silnik:")
        self.depth_label = QLabel("Ilość ruchów do przodu:")
        self.elo_label = QLabel("Elo (FIDE):")

        moves_sort_button = QPushButton()
        moves_sort_button.setFixedSize(40, 40)
        moves_sort_button.setCursor(QCursor(Qt.PointingHandCursor))
        moves_sort_button.setIcon(QIcon('../resources/up-and-down-arrow.png'))
        moves_sort_button.setIconSize(QSize(30, 30))
        moves_sort_button.setMenu(sort_menu)

        engine_settings_button = QPushButton(self)
        engine_settings_button.setFixedSize(40, 40)
        engine_settings_button.setObjectName("engine-settings")
        engine_settings_button.setIcon(QIcon('../resources/gear.png'))
        engine_settings_button.setIconSize(QSize(30, 30))
        engine_settings_button.setCursor(QCursor(Qt.PointingHandCursor))
        engine_settings_button.clicked.connect(self.settings_up)

        # Layouts parts
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(20, 0, 0, 0)
        left_layout.addWidget(self.engine_label)
        left_layout.addWidget(self.depth_label)
        left_layout.addWidget(self.elo_label)
        left_layout.setSpacing(85)

        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(moves_sort_button)
        right_layout.addWidget(engine_settings_button)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_widget.setFixedSize(100, 48)
        right_widget.setLayout(right_layout)

        # Layout
        self.engine_frame_layout = QHBoxLayout()
        self.engine_frame_layout.addWidget(left_widget)
        self.engine_frame_layout.addWidget(right_widget)
        self.engine_frame_layout.setContentsMargins(0, 0, 0, 0)

        # Frame
        self.setLayout(self.engine_frame_layout)
        self.setGeometry(0, 550, 1200, 50)
        self.setObjectName("engine-frame")
        self.setStyleSheet(f"""
            #engine-frame {{
                background-color: {color_theme[1]};
                border-top: 1px solid {color_theme[3]};
                border-bottom: 1px solid {color_theme[3]};
            }}
                
            QWidget {{
                background-color: {color_theme[1]};
                color: {color_theme[3]};
                font-size: 18px;
            }}
            
            QPushButton {{
                border: none;
            }}
            
            QPushButton::menu-indicator {{
                width: 0px;
            }}
            
            QPushButton:hover {{
                color: {color_theme[0]};
                background-color: {color_theme[3]};
                border: 1px solid {color_theme[0]};
                border-radius: 10px;
            }}
            
            QMenu {{
                color: {color_theme[3]};
                background-color: {color_theme[1]};
                border: 1px solid {color_theme[3]};
            }}
            
            QMenu::item {{
                padding: 5px 10px;
            }}
            
            QMenu::item:selected {{
                color: {color_theme[0]};
                background-color: {color_theme[1]};
            }}
            """)

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

    def update_theme(self, themes):
        style = f"""
            #engine-frame {{
                background-color: {themes[1]};
                border-top: 1px solid {themes[3]};
                border-bottom: 1px solid {themes[3]};
            }}
                
            QWidget {{
                background-color: {themes[1]};
                color: {themes[3]};
                font-size: 18px;
            }}
            
            QPushButton {{
                border: none;
            }}
            
            QPushButton::menu-indicator {{
                width: 0px;
            }}
            
            QPushButton:hover {{
                color: {themes[0]};
                background-color: {themes[3]};
                border: 1px solid {themes[0]};
                border-radius: 10px;
            }}
            
            QMenu {{
                color: {themes[3]};
                background-color: {themes[1]};
                border: 1px solid {themes[3]};
            }}
            
            QMenu::item {{
                padding: 5px 10px;
            }}
            
            QMenu::item:selected {{
                color: {themes[0]};
                background-color: {themes[1]};
            }}
            """
        self.setStyleSheet(style)