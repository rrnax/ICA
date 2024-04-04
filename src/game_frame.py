import math

from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QPen, QFont
from PyQt5.QtCore import Qt
from graphic_board import ChessBoard

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
        self.game_scene.draw_board((new_size.height() - 820) + 490)
        self.game_scene.resize_pieces()

# class ChessBoard(QGraphicsScene):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setSceneRect(0, 0, 750, 550)
#         self.fields_alph = ["A", "B", "C", "D", "E", "F", "G", "H"]
#         self.fields_num = ["1", "2", "3", "4", "5", "6", "7", "8"]
#         self.front_side = "white"
#         self.fields = []
#         self.init_board()
#
#     # Initial for board
#     def init_board(self):
#         for id_row, row in enumerate(self.fields_num):
#             for id_column, column in enumerate(self.fields_alph):
#                 field = Field(column+row)
#                 if (id_column + id_row) % 2 == 0:
#                     field.graphic_pos.setBrush(QColor(color_theme[3]))
#                 else:
#                     field.graphic_pos.setBrush(QColor(color_theme[4]))
#
#                 self.fields.append(field)
#         self.draw_board(480)
#
#     # Drawing board
#     def draw_board(self, side_length):
#         field_size = math.floor(side_length/8)
#         start_y = math.floor(self.height()/2 - side_length/2) + 10
#         start_x = math.floor(self.width()/2 + side_length/2) - field_size
#
#         if self.front_side == 'black':
#             last_row = self.fields[0].chess_pos[1]
#             for field in self.fields:
#                 if last_row != field.chess_pos[1]:
#                     last_row = field.chess_pos[1]
#                     start_x = math.floor(self.width() / 2 + side_length / 2) - field_size
#                     start_y += field_size
#
#                 if field.chess_pos[1] == "1":
#                     field.field_labels[1].setPos(start_x + field_size/2 - 9, start_y - 30)
#                     if field.unmounted:
#                         self.addItem(field.field_labels[1])
#
#                 if field.chess_pos[0] == "H":
#                     field.field_labels[0].setPos(start_x - field_size/2, start_y + field_size/2 - 18)
#                     if field.unmounted:
#                         self.addItem(field.field_labels[0])
#
#                 field.graphic_pos.setRect(start_x, start_y, field_size, field_size)
#                 start_x -= field_size
#
#                 if field.unmounted:
#                     self.addItem(field.graphic_pos)
#                     field.unmounted = False
#         else:
#             last_row = self.fields[-1].chess_pos[1]
#             for field in reversed(self.fields):
#
#                 if last_row != field.chess_pos[1]:
#                     last_row = field.chess_pos[1]
#                     start_x = math.floor(self.width() / 2 + side_length / 2) - field_size
#                     start_y += field_size
#
#                 if field.chess_pos[1] == "8":
#                     field.field_labels[1].setPos(start_x + field_size/2 - 9, start_y - 30)
#                     if field.unmounted:
#                         self.addItem(field.field_labels[1])
#
#                 if field.chess_pos[0] == "A":
#                     field.field_labels[0].setPos(start_x - field_size/2, start_y + field_size/2 - 18)
#                     if field.unmounted:
#                         self.addItem(field.field_labels[0])
#
#                 field.graphic_pos.setRect(start_x, start_y, field_size, field_size)
#                 start_x -= field_size
#
#                 if field.unmounted:
#                     self.addItem(field.graphic_pos)
#                     field.unmounted = False
#
#     def rotate_board(self):
#         for field in self.fields:
#             field.unmounted = True
#
#         for item in self.items():
#             self.removeItem(item)
#
#         if self.front_side == "white":
#             self.front_side = "black"
#         else:
#             self.front_side = "white"
#         self.draw_board(self.height() - 60)
#         self.update()
#
#
# class Field:
#     def __init__(self, chess_pos):
#         self.chess_pos = chess_pos
#         self.graphic_pos = QGraphicsRectItem()
#         self.field_labels = [QGraphicsTextItem(chess_pos[1]), QGraphicsTextItem(chess_pos[0])]
#         self.unmounted = True
#
#         # pen = QPen(Qt.NoPen)
#         # self.graphic_pos.setPen(pen)
#
#         font = QFont()
#         font.setPointSize(18)
#         for label in self.field_labels:
#             label.setFont(font)
#             label.setDefaultTextColor(QColor(color_theme[3]))
#
#
#
#
#
#
#
