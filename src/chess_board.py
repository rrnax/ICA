from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from math import floor
from chess import parse_square
from logic_board import LogicBoard
from piece import VirtualPiece
from field import VirtualField

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF", "#0022ff"]


class ChessBoard(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 750, 550)
        self.logic_board = LogicBoard()
        self.logic_board.graphic_board = self

        # Position left up corner on scene and board side length
        self.board_x = None
        self.board_y = None
        self.board_length = None

        # Dictionaries
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

        # Items and initial methods
        self.front_side = "white"
        self.fields = []
        self.pieces = []
        self.init_board()
        self.init_pieces()
        self.draw_pieces()

    # Initial board
    def init_board(self):
        # Enumerate via dictionaries to create correct fields
        for id_row, row in enumerate(self.fields_num):
            for id_column, column in enumerate(self.fields_alph):
                field = VirtualField(column + row)
                if (id_column + id_row) % 2 == 0:
                    field.setBrush(QColor(color_theme[3]))
                    field.orginal_brush = QColor(color_theme[3])
                else:
                    field.setBrush(QColor(color_theme[4]))
                    field.orginal_brush = QColor(color_theme[4])

                self.fields.append(field)
        self.draw_board(480)

    # Drawing board
    def draw_board(self, side_length):
        # Center of scene, start from right up corner minus one field
        field_size = floor(side_length / 8)
        start_y = floor(self.height() / 2 - side_length / 2) + 10
        start_x = floor(self.width() / 2 + side_length / 2) - field_size

        # Set board coordinates and size
        self.board_x = floor(self.width() / 2 - side_length / 2)
        self.board_y = start_y
        self.board_length = side_length

        # Place fields in dependence of chess side
        if self.front_side == 'black':
            last_row = self.fields[0].chess_pos[1]
            for field in self.fields:
                if last_row != field.chess_pos[1]:
                    last_row = field.chess_pos[1]
                    start_x = floor(self.width() / 2 + side_length / 2) - field_size
                    start_y += field_size

                if field.chess_pos[1] == "1":
                    field.field_labels[1].setPos(start_x + field_size / 2 - 9, start_y - 39)
                    if field.unmounted:
                        self.addItem(field.field_labels[1])

                if field.chess_pos[0] == "h":
                    field.field_labels[0].setPos(start_x - field_size / 2, start_y + field_size / 2 - 18)
                    if field.unmounted:
                        self.addItem(field.field_labels[0])

                field.setRect(start_x, start_y, field_size, field_size)
                start_x -= field_size

                if field.unmounted:
                    self.addItem(field)
                    field.unmounted = False
        else:
            last_row = self.fields[-1].chess_pos[1]
            for field in reversed(self.fields):

                if last_row != field.chess_pos[1]:
                    last_row = field.chess_pos[1]
                    start_x = floor(self.width() / 2 + side_length / 2) - field_size
                    start_y += field_size

                if field.chess_pos[1] == "8":
                    field.field_labels[1].setPos(start_x + field_size / 2 - 9, start_y - 39)
                    if field.unmounted:
                        self.addItem(field.field_labels[1])

                if field.chess_pos[0] == "a":
                    field.field_labels[0].setPos(start_x - field_size / 2, start_y + field_size / 2 - 18)
                    if field.unmounted:
                        self.addItem(field.field_labels[0])

                field.setRect(start_x, start_y, field_size, field_size)
                start_x -= field_size

                if field.unmounted:
                    self.addItem(field)
                    field.unmounted = False

    # Rotating board with all pieces
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

    # Create pieces from logic board for all fields
    def init_pieces(self):
        for field in self.fields:
            square_pos = parse_square(field.chess_pos)
            piece_fen = self.logic_board.piece_at(square_pos)
            if piece_fen is not None:
                for key, value in self.pieces_dict.items():
                    if value == piece_fen.symbol():
                        piece = VirtualPiece(key, value, field)
                        self.pieces.append(piece)

    # Scale and place pieces on scene
    def draw_pieces(self):
        for piece in self.pieces:
            if piece.fen_id == 'P' or piece.fen_id == 'p':
                piece.image = piece.image.scaled(floor(piece.field.rect().width() * 0.6),
                                                 floor(piece.field.rect().height() * 0.6),
                                                 Qt.KeepAspectRatio,
                                                 Qt.SmoothTransformation)

            else:
                piece.image = piece.image.scaled(floor(piece.field.rect().width() * 0.8),
                                                 floor(piece.field.rect().height() * 0.8),
                                                 Qt.KeepAspectRatio,
                                                 Qt.SmoothTransformation)

            piece.update_pixmap(piece.image)

            x = (piece.field.rect().x() +
                 (piece.field.rect().width() -
                  piece.image.width()) /
                 2.0)
            y = (piece.field.rect().y() +
                 (piece.field.rect().height() -
                  piece.image.height()) /
                 2.0)

            piece.set_position(x, y)
            self.addItem(piece)

    # During window size change or rotate
    def resize_pieces(self):
        for piece in self.pieces:
            if piece is not None:
                self.removeItem(piece)
        self.draw_pieces()

    def find_legal_fields(self, legal_moves):
        circle_size = floor(self.board_length/32)
        for field in self.fields:
            if field.chess_pos in legal_moves:
                self.addEllipse(field.rect().x() + (field.rect().width() - circle_size)/2,
                                field.rect().y() + (field.rect().height() - circle_size)/2,
                                circle_size,
                                circle_size,
                                pen=QColor(color_theme[5]),
                                brush=QColor(color_theme[5]))


