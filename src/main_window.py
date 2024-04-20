from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QCursor, QColor, QPen
from moves_options_widget import MovesOptionsList
from engine_frame import EngineFrame
from menu_widget import MenuSlideFrame
from stats_frame import StatsFrame
from game_frame import GameFrame
from logic_board import LogicBoard
from engine import ChessEngine
from sheard_memory import SharedMemoryStorage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic_board = LogicBoard()
        self.engine = ChessEngine()
        self.storage = SharedMemoryStorage()
        self.storage.initialize()

        # Window containers
        self.game_frame = GameFrame(self)
        self.menu_btn = QPushButton(self)
        self.menu_widget = MenuSlideFrame(self)
        self.stats_frame = StatsFrame(self)
        self.moves_frame = MovesOptionsList(self)
        self.engine_frame = EngineFrame(self)
        self.window_style = self.create_style()

        # Create basics for modules working
        self.assign_modules()
        self.set_items_properties()
        self.set_general_properties()
        self.setStyleSheet(self.window_style)
        self.logic_board.initial_workers()
        self.engine.initialize()
        self.logic_board.make_analyze()

        # Actions
        self.menu_btn.clicked.connect(self.menu_widget.open_menu)
        self.menu_widget.raise_()

    def set_general_properties(self):
        self.setMinimumSize(QSize(1200, 820))
        self.setWindowTitle("Interaktywny Asystent Szachowy")
        self.setObjectName('main-window')

    # Assign correct modules to containers
    def assign_modules(self):
        self.logic_board.game_widget = self.game_frame
        self.logic_board.stats_frame = self.stats_frame
        self.logic_board.graphic_board = self.game_frame.game_scene
        self.stats_frame.graphic_board = self.game_frame.game_scene
        self.engine.graphic_board = self.game_frame.game_scene
        self.engine.moves_frame = self.moves_frame
        self.engine.engine_frame = self.engine_frame

    def set_items_properties(self):
        # Button for open
        self.menu_btn.setIcon(QIcon('../resources/menu.png'))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.menu_btn.setGeometry(10, 10, 50, 50)
        self.menu_btn.setObjectName("menu-btn")

    def resizeEvent(self, event):
        self.upadte_sizes()

    def upadte_sizes(self):
        self.game_frame.update_size(self.size())
        self.menu_widget.update_size(self.size())
        self.stats_frame.update_size(self.size())
        self.engine_frame.update_size(self.size())
        self.moves_frame.update_size(self.size())

    def closeEvent(self, event):
        self.engine.close_connect()
        event.accept()

    # Method change all containers in app
    def change_theme(self):
        if self.menu_widget.veify_state():
            self.storage.set_light()
        else:
            self.storage.set_dark()

        # This container
        style = self.create_style()
        self.setStyleSheet(style)

        # Other
        self.menu_widget.update_style()
        self.game_frame.update_theme()
        self.stats_frame.update_theme()
        self.engine_frame.update_theme()
        self.moves_frame.update_theme()

    # Produce style for this container
    def create_style(self):
        return f"""
            #main-window {{
                background-color: {self.storage.color_theme[0]};
            }}
            
            #menu-btn {{
                background-color: {self.storage.color_theme[1]};
                border: 2px solid {self.storage.color_theme[3]};
                border-radius: 5px;
            }}
            
            #menu-btn:hover {{
                background-color: {self.storage.color_theme[3]};
            }}
        """

