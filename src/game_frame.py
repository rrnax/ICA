import math

from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QPen, QFont
from PyQt5.QtCore import Qt

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
        self.game_view.setBackgroundBrush(QColor(color_theme[0]))
        self.game_view.setObjectName("game-frame")

    def update_size(self, new_size):
        self.setGeometry(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_view.setFixedSize((new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.setSceneRect(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)


class ChessBoard(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 750, 550)
        self.fields_alph = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.fields_num = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.draw_board(480)

    def draw_board(self, side_length):

        field_size = math.floor(side_length/8)

        start_x = math.floor(self.width()/2 - 4 * field_size)
        start_y = math.floor(self.height()/2 - 4 * field_size) + 10

        for row in range(0, 9):
            for column in range(0, 9):
                field = None
                if column == 0 or row == 0:
                    color = QColor(color_theme[0])
                    if not (column == 0 and row == 0):
                        label = None
                        if column == 0:
                            label = QGraphicsTextItem(self.fields_num[row-1])
                            label.setPos(start_x + ((column - 1) * field_size) + field_size/2, start_y + (row - 1) * field_size )
                            font = QFont()
                            font.setPointSize(18)
                            label.setFont(font)
                            label.setDefaultTextColor(QColor(color_theme[3]))
                        elif row == 0:
                            label = QGraphicsTextItem(self.fields_alph[column - 1])
                            label.setPos(start_x + ((column - 1) * field_size) + field_size / 2,
                                         start_y + (row - 1) * field_size + field_size / 2 - 10)
                            font = QFont()
                            font.setPointSize(18)
                            label.setFont(font)
                            label.setDefaultTextColor(QColor(color_theme[3]))

                        self.addItem(label)
                else:
                    if (row + column) % 2 == 0:
                        color = QColor("#f5f2f2")
                    else:
                        color = QColor(color_theme[3])
                    field = QGraphicsRectItem(start_x + ((column - 1) * field_size), start_y + (row - 1) * field_size,
                                              field_size, field_size)
                    field.setBrush(color)
                    self.addItem(field)

