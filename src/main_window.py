from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from engine_frame import EngineFrame

color_theme = ["#191A19", "#1E5128", "#4E9F3D", "#D8E9A8", "#FFFFFF"]


class MainWindow(QMainWindow):

    def __init__(self):
        # Window settings
        super().__init__()
        self.setWindowTitle("Interactive Chess assistant")
        self.setMinimumSize(QSize(1200, 820))
        self.setStyleSheet(f"background-color: {color_theme[0]};")

        general_widget = QWidget()

        self.game_frame = QFrame(self)
        self.game_frame.setGeometry(0, 0, 750, 550)
        # self.game_frame.setStyleSheet("QFrame { border-radius: 100px; border: 2px solid blue; }")

        self.stats_frame = QFrame(self)
        self.stats_frame.setGeometry(750, 0, 450, 550)
        self.stats_frame.setStyleSheet(f"border-left: 1px solid {color_theme[3]};")

        self.engine_frame = EngineFrame(self)

        game_scene = QGraphicsScene()
        self.game_view = QGraphicsView(game_scene, self.game_frame)
        self.game_view.setStyleSheet(f"border: none")
        self.game_view.setBackgroundBrush(QColor(0, 0, 0))

        self.moves_frame = QListWidget(self)
        self.moves_frame.setGeometry(0, 620, 1200, 200)
        self.moves_frame.setStyleSheet(f"border: none;")

    def resizeEvent(self, event):
        self.upadte_sizes()

    def upadte_sizes(self):
        self.game_frame.resize((self.size().width() - 1200) + 750, (self.size().height() - 820) + 550)
        self.game_view.setGeometry(self.game_frame.rect())
        self.stats_frame.setGeometry((self.size().width() - 1200) + 750, 0, 450, (self.size().height() - 820) + 550)
        self.moves_frame.setGeometry(0, (self.size().height() - 820) + 620, (self.size().width() - 1200) + 1200, 200)
        self.engine_frame.change_for_window_resize(self.size())


