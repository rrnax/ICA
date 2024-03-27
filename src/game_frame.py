import math

from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QColor

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
        self.game_view.setFixedSize(750, 550)
        self.game_view.setBackgroundBrush(QColor(0, 0, 0))
        self.game_view.setObjectName("game-frame")

    def update_size(self, new_size):
        self.setGeometry(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_view.setFixedSize((new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.setSceneRect(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)


class ChessBoard(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 750, 550)
        self.draw_board(490)

    def draw_board(self, side_length):

        field_size = math.floor(side_length/8)

        start_x = math.floor(self.width()/2 - 4 * field_size)
        start_y = math.floor(self.height()/2 - 4 * field_size)

        for row in range(1, 9):
            for column in range(0, 8):
                if (row + column) % 2 == 0:
                    color = QColor(color_theme[4])
                else:
                    color = QColor(color_theme[3])
                field = QGraphicsRectItem(start_x + (column * field_size), start_y + (row-1) * field_size, field_size, field_size)
                field.setBrush(color)
                self.addItem(field)
