from PyQt5.QtWidgets import QFrame, QGraphicsView
from PyQt5.QtGui import QColor, QPainter
from chess_board import ChessBoard

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class GameFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 750, 550)
        self.setStyleSheet(f"""
                    #game-frame {{
                        border: none;
                    }}
                """)

        self.game_scene = ChessBoard(self)
        self.game_view = QGraphicsView(self.game_scene, self)
        self.game_view.setRenderHint(QPainter.Antialiasing)
        self.game_view.setFixedSize(750, 550)
        self.game_view.setBackgroundBrush(QColor(color_theme[0]))
        self.game_view.setObjectName("game-frame")

    def update_size(self, new_size):
        self.setGeometry(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_view.setFixedSize((new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.setSceneRect(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.draw_board((new_size.height() - 820) + 490)
        self.game_scene.resize_pieces()

