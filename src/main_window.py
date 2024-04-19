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
from sheard_memory import color_theme


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic_board = LogicBoard()
        self.engine = ChessEngine()

        # View with board
        self.game_frame = GameFrame(self)
        self.logic_board.game_widget = self.game_frame

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
        self.logic_board.stats_frame = self.stats_frame
        self.logic_board.graphic_board = self.game_frame.game_scene
        self.stats_frame.graphic_board = self.game_frame.game_scene
        self.engine.graphic_board = self.game_frame.game_scene

        # Frame with result of move options
        self.moves_frame = MovesOptionsList(self)
        self.engine.moves_frame = self.moves_frame

        # Frame with settings of chess engine
        self.engine_frame = EngineFrame(self)
        self.engine.engine_frame = self.engine_frame

        # Sets main window
        self.setMinimumSize(QSize(1200, 820))
        self.setWindowTitle("Interaktywny Asystent Szachowy")
        self.setObjectName('main-window')
        self.window_style = f"""
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
        """
        self.setStyleSheet(self.window_style)

        self.logic_board.initial_workers()
        self.engine.initialize()
        self.logic_board.make_analyze()

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

    def closeEvent(self, event):
        self.engine.close_connect()
        event.accept()

    def change_theme(self, themes):
        style = f"""
            #main-window {{
                background-color: {themes[0]};
            }}

            #menu-btn {{
                background-color: {themes[1]};
                border: 2px solid {themes[3]};
                border-radius: 5px;
            }}

            #menu-btn:hover {{
                background-color: {themes[3]};
            }}
        """
        self.setStyleSheet(style)
        self.game_frame.game_view.setBackgroundBrush(QColor(themes[0]))
        for field in self.game_frame.game_scene.fields:
            field.field_labels[0].setDefaultTextColor(QColor(themes[3]))
            field.field_labels[1].setDefaultTextColor(QColor(themes[3]))
            if themes[0] == "#1E1F22":
                pen = QPen(Qt.NoPen)
                field.setPen(pen)
            else:
                pen = QPen(QColor(themes[3]))
                field.setPen(pen)

        self.stats_frame.update_theme(themes)
        self.engine_frame.update_theme(themes)
        self.moves_frame.update_theme(themes)