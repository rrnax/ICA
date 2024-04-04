import math
import chess

from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import QSize, Qt, QPointF
from piece import VirtualPiece

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class ChessBoard(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.board = chess.Board()

        self.board_x = None
        self.board_y = None
        self.board_length = None

        self.setSceneRect(0, 0, 750, 550)
        self.fields_alph = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.fields_num = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.pieces_dict = {"w_king": "K",
                            "w_pawn": "P",
                            "w_rook": "R",
                            "w_knight": "N",
                            "w_bishop": "B",
                            "w_queen": "Q",
                            "b_king": "k",
                            "b_pawn": "p",
                            "b_rook": "r",
                            "b_knight": "n",
                            "b_bishop": "b",
                            "b_queen": "q"
                            }
        self.front_side = "white"
        self.fields = []
        self.pieces = []
        self.init_board()
        self.init_pieces()
        self.draw_pieces()

    # Initial for board
    def init_board(self):
        for id_row, row in enumerate(self.fields_num):
            for id_column, column in enumerate(self.fields_alph):
                field = Field(column + row)
                if (id_column + id_row) % 2 == 0:
                    field.graphic_pos.setBrush(QColor(color_theme[3]))
                    field.orginal_brush = QColor(color_theme[3])
                else:
                    field.graphic_pos.setBrush(QColor(color_theme[4]))
                    field.orginal_brush = QColor(color_theme[4])

                self.fields.append(field)
        self.draw_board(480)

    # Drawing board
    def draw_board(self, side_length):
        field_size = math.floor(side_length / 8)
        start_y = math.floor(self.height() / 2 - side_length / 2) + 10
        start_x = math.floor(self.width() / 2 + side_length / 2) - field_size

        self.board_x = math.floor(self.width() / 2 - side_length / 2)
        self.board_y = start_y
        self.board_length = side_length

        if self.front_side == 'black':
            last_row = self.fields[0].chess_pos[1]
            for field in self.fields:
                if last_row != field.chess_pos[1]:
                    last_row = field.chess_pos[1]
                    start_x = math.floor(self.width() / 2 + side_length / 2) - field_size
                    start_y += field_size

                if field.chess_pos[1] == "1":
                    field.field_labels[1].setPos(start_x + field_size / 2 - 9, start_y - 39)
                    if field.unmounted:
                        self.addItem(field.field_labels[1])

                if field.chess_pos[0] == "h":
                    field.field_labels[0].setPos(start_x - field_size / 2, start_y + field_size / 2 - 18)
                    if field.unmounted:
                        self.addItem(field.field_labels[0])

                field.graphic_pos.setRect(start_x, start_y, field_size, field_size)
                start_x -= field_size

                if field.unmounted:
                    self.addItem(field.graphic_pos)
                    field.unmounted = False
        else:
            last_row = self.fields[-1].chess_pos[1]
            for field in reversed(self.fields):

                if last_row != field.chess_pos[1]:
                    last_row = field.chess_pos[1]
                    start_x = math.floor(self.width() / 2 + side_length / 2) - field_size
                    start_y += field_size

                if field.chess_pos[1] == "8":
                    field.field_labels[1].setPos(start_x + field_size / 2 - 9, start_y - 39)
                    if field.unmounted:
                        self.addItem(field.field_labels[1])

                if field.chess_pos[0] == "a":
                    field.field_labels[0].setPos(start_x - field_size / 2, start_y + field_size / 2 - 18)
                    if field.unmounted:
                        self.addItem(field.field_labels[0])

                field.graphic_pos.setRect(start_x, start_y, field_size, field_size)
                start_x -= field_size

                if field.unmounted:
                    self.addItem(field.graphic_pos)
                    field.unmounted = False

    def rotate_board(self):
        for field in self.fields:
            field.unmounted = True

        for item in self.items():
            self.removeItem(item)

        if self.front_side == "white":
            self.front_side = "black"
        else:
            self.front_side = "white"
        self.draw_board(self.height() - 60)
        self.resize_pieces()

    def init_pieces(self):

        for field in self.fields:
            square_pos = chess.parse_square(field.chess_pos)
            piece_fen = self.board.piece_at(square_pos)
            if piece_fen is not None:
                for key, value in self.pieces_dict.items():
                    if value == piece_fen.symbol():
                        piece = VirtualPiece(key, value, field)
                        self.pieces.append(piece)

    def draw_pieces(self):
        for piece in self.pieces:
            if piece.fen_id == 'P' or piece.fen_id == 'p':
                piece.image = piece.image.scaled(math.floor(piece.field.graphic_pos.rect().width() * 0.6),
                                                 math.floor(piece.field.graphic_pos.rect().height() * 0.6),
                                                 Qt.KeepAspectRatio,
                                                 Qt.SmoothTransformation)

            else:
                piece.image = piece.image.scaled(math.floor(piece.field.graphic_pos.rect().width() * 0.8),
                                                 math.floor(piece.field.graphic_pos.rect().height() * 0.8),
                                                 Qt.KeepAspectRatio,
                                                 Qt.SmoothTransformation)

            piece.update_pixmap(piece.image)

            x = (piece.field.graphic_pos.rect().x() +
                 (piece.field.graphic_pos.rect().width() -
                  piece.image.width()) /
                 2.0)
            y = (piece.field.graphic_pos.rect().y() +
                 (piece.field.graphic_pos.rect().height() -
                  piece.image.height()) /
                 2.0)

            piece.set_position(x, y)
            self.addItem(piece)

    def resize_pieces(self):
        for piece in self.pieces:
            if piece is not None:
                self.removeItem(piece)
        self.draw_pieces()


class Field:
    def __init__(self, chess_pos):
        self.chess_pos = chess_pos
        self.orginal_brush = None
        self.graphic_pos = QGraphicsRectItem()
        self.field_labels = [QGraphicsTextItem(chess_pos[1]), QGraphicsTextItem(chess_pos[0].upper())]
        self.unmounted = True
        self.brushed = False

        # pen = QPen(Qt.NoPen)
        # self.graphic_pos.setPen(pen)

        font = QFont()
        font.setPointSize(18)
        for label in self.field_labels:
            label.setFont(font)
            label.setDefaultTextColor(QColor(color_theme[3]))


