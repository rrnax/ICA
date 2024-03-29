from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QCursor
from moves_options_widget import MovesOptionsList
from engine_frame import EngineFrame
from menu_widget import MenuSlideFrame
from stats_frame import StatsFrame
from game_frame import GameFrame

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # View with board
        self.game_frame = GameFrame(self)

        # Panel with menu of app and button to open menu
        menu_btn = QPushButton(self)
        menu_btn.setIcon(QIcon('../resources/menu.png'))
        menu_btn.setIconSize(QSize(30, 30))
        menu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        menu_btn.setGeometry(10, 10, 50, 50)
        menu_btn.setObjectName("menu-btn")
        self.menu_widget = MenuSlideFrame(self)

        # Frame with progress and stats of current game
        self.stats_frame = StatsFrame(self)

        # Frame with result of move options
        self.moves_frame = MovesOptionsList(self)

        # Frame with settings of chess engine
        self.engine_frame = EngineFrame(self)

        # Sets main window
        self.setMinimumSize(QSize(1200, 820))
        self.setWindowTitle("Interaktywny Asystent Szachowy")
        self.setObjectName('main-window')
        self.setStyleSheet(f"""
            #main-window {{
                background-color: {color_theme[0]};
            }}
            
            #menu-btn {{
                background-color: {color_theme[1]};
                border: 2px solid {color_theme[3]};
                border-radius: 5px;
            }}
            
            #menu-btn:hover {{
                background-color: {color_theme[3]};
            }}
        """)

        # Actions
        menu_btn.clicked.connect(self.menu_widget.open_menu)
        self.menu_widget.raise_()

    # If window is changed
    def resizeEvent(self, event):
        self.upadte_sizes()

    def upadte_sizes(self):
        self.game_frame.update_size(self.size())
        self.menu_widget.update_size(self.size())
        self.stats_frame.update_size(self.size())
        self.engine_frame.update_size(self.size())
        self.moves_frame.update_size(self.size())
