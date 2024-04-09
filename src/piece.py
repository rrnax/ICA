from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from logic_board import LogicBoard
from chess import Move, square_name

# Here are contribution license links fo images
# <a href="https://www.flaticon.com/free-icons/chess-piece" title="chess piece icons">Chess piece icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by deemakdaksina - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by Stockio - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by SBTS2018 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/tactic" title="tactic icons">Tactic icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/bishop" title="bishop icons">Bishop icons created by Victoruler - Flaticon</a>


class VirtualPiece(QGraphicsPixmapItem):
    def __init__(self, name, value, field, graphic_board):
        super().__init__()
        self.setZValue(3)
        self.setAcceptHoverEvents(True)
        self.logic_board = LogicBoard()
        self.graphic_board = graphic_board

        self.name = name
        self.fen_id = value
        self.previous_fields = []
        self.current_field = field
        self.image = None
        self.legal_fields = None
        self.last_move = None
        self.set_image()

    # Deal with piece images
    def set_image(self):
        path = "../resources/pieces/" + self.name + ".png"
        self.image = QPixmap(path)
        if self.image is not None:
            self.setPixmap(self.image)

    def update_pixmap(self, pixmap):
        if pixmap is not None:
            self.setPixmap(pixmap)

    # Mouse on piece events
    def hoverEnterEvent(self, event):
        if self.logic_board.check_turn(self.name[0]):
            self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if self.logic_board.check_turn(self.name[0]):
            self.legal_fields = self.logic_board.find_possible_fields(self.current_field.chess_pos)
            self.graphic_board.highlight_field(self.current_field)
            self.graphic_board.mark_legal_fields(self.legal_fields, self.current_field)
            self.setCursor(Qt.ClosedHandCursor)

    def mouseDoubleClickEvent(self, event):
        if self.logic_board.check_turn(self.name[0]):
            self.graphic_board.clear_highlighted()
            self.graphic_board.clear_circles()
            self.graphic_board.clear_captures()

    def mouseMoveEvent(self, event):
        if self.logic_board.check_turn(self.name[0]):
            self.setPos(self.new_piece_position(event))

    def mouseReleaseEvent(self, event):
        # Check position on board or outside
        if self.logic_board.check_turn(self.name[0]):
            piece_position = self.new_piece_position(event)
            target_field = self.match_field(piece_position)
            if target_field is not None:
                self.graphic_move(target_field)
                self.make_move()
            else:
                self.set_in_field(self.current_field)

            self.setCursor(Qt.OpenHandCursor)

    # Making move operations
    def make_move(self):
        additional_info = self.logic_board.find_info(self.last_move)
        self.logic_board.push(self.last_move)
        temp = self.logic_board.check_end()
        if additional_info != "" and temp != "":
            additional_info += "\n"
        additional_info += temp
        self.logic_board.advanced_move(self, self.last_move, additional_info)
        self.logic_board.update_history()

    # Create position on mouse base movement
    def new_piece_position(self, event):
        last_mouse_position = event.lastScenePos()
        new_mouse_position = event.scenePos()
        last_piece_position = self.scenePos()

        new_x = new_mouse_position.x() - last_mouse_position.x() + last_piece_position.x()
        new_y = new_mouse_position.y() - last_mouse_position.y() + last_piece_position.y()
        return QPointF(new_x, new_y)

    # Animate graphic move on board
    def graphic_move(self, field):
        move_uci = self.current_field.chess_pos + field.chess_pos
        self.last_move = Move.from_uci(move_uci)
        self.move_validation(self.last_move)
        self.previous_fields.append(self.current_field)
        self.current_field = field
        self.set_in_field(field)
        self.graphic_board.clear_captures()
        self.graphic_board.clear_circles()

    # Find field for piece by coordinates
    def match_field(self, piece_position):
        if not ((piece_position.x() +
                 self.image.width() / 2 >=
                 self.graphic_board.board_x +
                 self.graphic_board.board_length
                 or piece_position.y() +
                 self.image.height() / 2 >=
                 self.graphic_board.board_y +
                 self.graphic_board.board_length)
                or (piece_position.x() +
                    self.image.width() / 2 <=
                    self.graphic_board.board_x
                    or piece_position.y() +
                    self.image.height() / 2 <=
                    self.graphic_board.board_y)):

            for field in self.legal_fields:

                left_up_corner = QPointF(field.rect().x(),
                                         field.rect().y())
                right_down_corner = QPointF(field.rect().x() +
                                            field.rect().width(),
                                            field.rect().y() +
                                            field.rect().height())

                if ((left_up_corner.x() <= piece_position.x() +
                     self.image.width() / 2 <= right_down_corner.x())
                        and (left_up_corner.y() <= piece_position.y() +
                             self.image.height() / 2 <= right_down_corner.y())):
                    return field
        return None

    # Find correct position in field
    def set_in_field(self, field):
        x = (field.rect().x() +
             (field.rect().width() -
              self.image.width()) /
             2.0)
        y = (field.rect().y() +
             (field.rect().height() -
              self.image.height()) /
             2.0)
        self.setPos(x, y)

    # Make validation before move for correct operations
    def move_validation(self, move):
        self.graphic_board.remove_check()
        if self.logic_board.is_castling(move):
            self.make_castling(move)

        if self.logic_board.gives_check(move):
            self.graphic_board.make_check()

        if self.logic_board.is_capture(move):
            field_id = square_name(move.to_square)
            self.graphic_board.remove_captured(field_id)

    # Deal with castling move
    def make_castling(self, move):
        if self.logic_board.is_kingside_castling(move):
            if self.logic_board.turn:
                rook = self.graphic_board.find_piece_by_id("h1")
                target_field = self.graphic_board.find_field("f1")
                rook.graphic_move(target_field)
            else:
                rook = self.graphic_board.find_piece_by_id("h8")
                target_field = self.graphic_board.find_field("f8")
                rook.graphic_move(target_field)
        elif self.logic_board.is_queenside_castling(move):
            if self.logic_board.turn:
                rook = self.graphic_board.find_piece_by_id("a1")
                target_field = self.graphic_board.find_field("d1")
                rook.graphic_move(target_field)
            else:
                rook = self.graphic_board.find_piece_by_id("a8")
                target_field = self.graphic_board.find_field("d8")
                rook.graphic_move(target_field)

    def undo_castling(self, move):
        if self.logic_board.is_kingside_castling(move):
            if self.logic_board.turn:
                rook = self.graphic_board.find_piece_by_id("f1")
                rook.undo_last_move()
            else:
                rook = self.graphic_board.find_piece_by_id("f8")
                rook.undo_last_move()
        elif self.logic_board.is_queenside_castling(move):
            if self.logic_board.turn:
                rook = self.graphic_board.find_piece_by_id("d1")
                rook.undo_last_move()
            else:
                rook = self.graphic_board.find_piece_by_id("d8")
                rook.undo_last_move()

    def undo_last_move(self):
        if self.previous_fields:
            last_field = self.previous_fields.pop()
            self.set_in_field(last_field)
            self.current_field = last_field
            if self.previous_fields:
                move_uci = self.previous_fields[-1].chess_pos + last_field.chess_pos
                self.last_move = Move.from_uci(move_uci)


