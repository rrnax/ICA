from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from math import floor
from chess import parse_square, Move
from logic_board import LogicBoard
from piece import VirtualPiece
from field import VirtualField

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF", "#96b3e0", "#bd755c"]


class ChessBoard(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 750, 550)
        self.logic_board = LogicBoard()

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
        self.circles = []
        self.capture_fields = []
        self.captured_pieces = []
        self.highlited_field = None
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

        if self.highlited_field is not None:
            last_piece = self.find_piece_by_id(self.highlited_field.chess_pos)
            if last_piece is not None:
                self.mark_legal_fields(last_piece.legal_fields, last_piece.current_field)

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
                        piece = VirtualPiece(key, value, field, self)
                        self.pieces.append(piece)

    # Scale and place pieces on scene
    def draw_pieces(self):
        for piece in self.pieces:
            if piece.current_field is not None:
                if piece.fen_id == 'P' or piece.fen_id == 'p':
                    piece.set_image()
                    piece.image = piece.image.scaled(floor(piece.current_field.rect().width() * 0.6),
                                                     floor(piece.current_field.rect().height() * 0.6),
                                                     Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)

                else:
                    piece.set_image()
                    piece.image = piece.image.scaled(floor(piece.current_field.rect().width() * 0.8),
                                                     floor(piece.current_field.rect().height() * 0.8),
                                                     Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)

                piece.update_pixmap(piece.image)

                x = (piece.current_field.rect().x() +
                     (piece.current_field.rect().width() -
                      piece.image.width()) /
                     2.0)
                y = (piece.current_field.rect().y() +
                     (piece.current_field.rect().height() -
                      piece.image.height()) /
                     2.0)

                piece.setPos(x, y)
                self.addItem(piece)

    # During window size change or rotate
    def resize_pieces(self):
        for piece in self.pieces:
            if piece is not None:
                self.removeItem(piece)
        self.draw_pieces()

    ####################################

    # Color possible field for optional moves by chose piece
    def mark_legal_fields(self, legal_fields, field_from):
        self.clear_captures()
        self.clear_circles()
        for field in legal_fields:
            move_uci = field_from.chess_pos + field.chess_pos
            if self.logic_board.is_capture(Move.from_uci(move_uci)):
                field.setBrush(QColor(color_theme[6]))
                self.capture_fields.append(field)
            else:
                self.draw_circle(field)

    # Operations with circles
    def draw_circle(self, field):
        circle_size = floor(self.board_length / 32)
        circle = self.addEllipse(field.rect().x() + (field.rect().width() - circle_size) / 2,
                                 field.rect().y() + (field.rect().height() - circle_size) / 2,
                                 circle_size,
                                 circle_size,
                                 pen=QColor(color_theme[5]),
                                 brush=QColor(color_theme[5]))
        self.circles.append(circle)

    def clear_circles(self):
        if self.circles:
            for circle in self.circles:
                self.removeItem(circle)
            self.circles.clear()

    # Operation with capture and last move trace
    def clear_captures(self):
        if self.capture_fields:
            for capture in self.capture_fields:
                capture.setBrush(QColor(capture.orginal_brush))
            self.capture_fields.clear()

    def remove_captured(self, field_id):
        captured_piece = self.find_piece_by_id(field_id)
        self.removeItem(captured_piece)
        self.pieces.remove(captured_piece)
        self.captured_pieces.append(captured_piece)

    def highlight_field(self, field):
        if self.highlited_field is not None:
            self.highlited_field.setBrush(QColor(self.highlited_field.orginal_brush))
        self.highlited_field = field
        field.setBrush(QColor(color_theme[5]))

    def clear_highlighted(self):
        if self.highlited_field is not None:
            self.highlited_field.setBrush(QColor(self.highlited_field.orginal_brush))
            self.highlited_field = None

    # Finding fields and pieces
    def find_field(self, field_id):
        for field in self.fields:
            if field.chess_pos == field_id:
                return field
        return None

    def find_piece_by_name(self, name):
        for piece in self.pieces:
            if piece.name == name:
                return piece
        return None

    def find_piece_by_id(self, field_id):
        field = self.find_field(field_id)
        for piece in self.pieces:
            if piece.current_field == field:
                return piece
        return None

    # Dealing graphic check
    def make_check(self):
        if self.logic_board.turn:
            king = self.find_piece_by_name("b_king")
        else:
            king = self.find_piece_by_name("w_king")
        king.current_field.setBrush(QColor(color_theme[6]))

    def remove_check(self):
        if self.logic_board.turn:
            king = self.find_piece_by_name("w_king")
        else:
            king = self.find_piece_by_name("b_king")
        king.current_field.setBrush(QColor(king.current_field.orginal_brush))

    def clear_check(self):
        king = self.find_piece_by_name("w_king")
        if king is not None:
            king.current_field.setBrush(QColor(king.current_field.orginal_brush))
        king = self.find_piece_by_name("b_king")
        if king is not None:
            king.current_field.setBrush(QColor(king.current_field.orginal_brush))

    def remove_undo_check(self):
        if self.logic_board.turn:
            king = self.find_piece_by_name("b_king")
        else:
            king = self.find_piece_by_name("w_king")
        king.current_field.setBrush(QColor(king.current_field.orginal_brush))

    # Clear graphic board to start position
    def clear_pieces(self):
        for piece in self.pieces:
            self.removeItem(piece)
        self.pieces.clear()
        self.captured_pieces.clear()
        self.clear_circles()
        self.clear_captures()
        self.clear_highlighted()

    def undo_castling(self, move):
        if self.logic_board.is_kingside_castling(move):
            if self.logic_board.turn:
                rook = self.find_piece_by_id("f1")
                rook.undo_last_move()
            else:
                rook = self.find_piece_by_id("f8")
                rook.undo_last_move()
        elif self.logic_board.is_queenside_castling(move):
            if self.logic_board.turn:
                rook = self.find_piece_by_id("d1")
                rook.undo_last_move()
            else:
                rook = self.find_piece_by_id("d8")
                rook.undo_last_move()

    def undo_capture(self):
        last_captured = self.captured_pieces.pop()
        self.addItem(last_captured)
        last_captured.set_in_field(last_captured.current_field)
        self.pieces.append(last_captured)
