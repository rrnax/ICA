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
        self.game_scene.draw_board()
        self.game_view = QGraphicsView(self.game_scene, self)
        self.game_view.setFixedSize(750, 550)
        self.game_view.setBackgroundBrush(QColor(0, 0, 0))
        self.game_view.setObjectName("game-frame")

    def update_size(self, new_size):
        self.setGeometry(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_view.setFixedSize((new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)


class ChessBoard(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

    def draw_board(self, side_length):
        r = QGraphicsRectItem(50, 50, 50, 50)
        r.setBrush(QColor(color_theme[3]))
        self.addItem(r)
        # for row in range(1, 9):
        #     for column in range(0, 8):
