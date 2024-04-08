from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem
from logic_board import LogicBoard
from chess import Move

# Here are contribution license links fo images
# <a href="https://www.flaticon.com/free-icons/chess-piece" title="chess piece icons">Chess piece icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by deemakdaksina - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by Stockio - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by SBTS2018 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/tactic" title="tactic icons">Tactic icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/bishop" title="bishop icons">Bishop icons created by Victoruler - Flaticon</a>

# Position highlighting colors
highlight = ["#96b3e0"]


class VirtualPiece(QGraphicsPixmapItem):
    def __init__(self, name, value, field, graphic_board):
        super().__init__()
        self.setZValue(3)
        self.setAcceptHoverEvents(True)
        self.logic_board = LogicBoard()
        self.graphic_board = graphic_board

        self.name = name
        self.fen_id = value
        self.last_field = None
        self.current_field = field
        self.image = None
        self.legal_fields = None
        self.lastPos = None
        self.captured_pos = None
        self.set_image()

    def set_image(self):
        path = "../resources/pieces/" + self.name + ".png"
        self.image = QPixmap(path)
        if self.image is not None:
            self.setPixmap(self.image)

    def set_position(self, x, y):
        self.setPos(x, y)
        self.lastPos = QPointF(x, y)

    def update_pixmap(self, pixmap):
        if pixmap is not None:
            self.setPixmap(pixmap)

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
            # chess_board = self.logic_board.graphic_board
            # if ((new_pos.x() + self.image.width()/2 >= chess_board.board_x + chess_board.board_length
            #      or new_pos.y() + self.image.height()/2 >= chess_board.board_y + chess_board.board_length)
            #         or (new_pos.x() + self.image.width()/2 <= chess_board.board_x
            #             or new_pos.y() + self.image.height()/2 <= chess_board.board_y)):
            #     self.setPos(self.lastPos)
            # else:
            #     # Check position for field on board
            #     for field in chess_board.fields:
            #         if field.chess_pos in self.legal_fields:
            #             start_pos = QPointF(field.rect().x(),
            #                                 field.rect().y())
            #             end_pos = QPointF(field.rect().x() +
            #                               field.rect().width(),
            #                               field.rect().y() +
            #                               field.rect().height())
            #
            #             if ((start_pos.x() <= new_pos.x() + self.image.width()/2 <= end_pos.x())
            #                     and (start_pos.y() <= new_pos.y() + self.image.height()/2 <= end_pos.y())):

            # move = Move.from_uci(self.last_field.chess_pos + self.current_field.chess_pos)
            #
            # if self.logic_board.is_capture(move):
            #     self.graphic_board.find_capture_piece(self.current_field.chess_pos)
            # if self.fen_id != 'K' and self.fen_id != 'k':
            #     self.graphic_board.clear_check()
            # self.graphic_board.check_castling(move)
            # self.graphic_board.clear_circles()
            # self.graphic_board.clear_captures()

            # Place piece on correct field
            # x = (field.rect().x() +
            #      (field.rect().width() -
            #       self.image.width()) /
            #      2.0)
            # y = (field.rect().y() +
            #      (field.rect().height() -
            #       self.image.height()) /
            #      2.0)

            # add_info = self.logic_board.find_info(move)
            #
            # self.logic_board.push(move)
            # self.set_position(x, y)
            # self.field = field
            # print(self.field.chess_pos)
            # chess_board.legal_moves = None
            # self.graphic_board.find_check()
            # self.logic_board.check_end()
            #
            # self.logic_board.advanced_move(self, move, add_info)
            # self.logic_board.stats_frame.update_history()

            # else:
            # self.setPos(self.lastPos)
    def upalumpa(self):
        move = Move.from_uci(self.last_field.chess_pos + self.current_field.chess_pos)
        # if self.logic_board.is_capture(move):
        #     self.graphic_board.find_capture_piece(self.current_field.chess_pos)
        # if self.fen_id != 'K' and self.fen_id != 'k':
        #     self.graphic_board.clear_check()
        # self.graphic_board.check_castling(move)
        # self.graphic_board.clear_circles()
        # self.graphic_board.clear_captures()
        add_info = self.logic_board.find_info(move)

        self.logic_board.push(move)
        self.graphic_board.find_check()
        self.logic_board.check_end()

        self.logic_board.advanced_move(self, move, add_info)
        self.logic_board.stats_frame.update_history()

    def make_move(self):
        move_uci = self.last_field.chess_pos + self.current_field.chess_pos
        move = Move.from_uci(move_uci)
        additional_info = self.logic_board.find_info(move)
        self.logic_board.push(move)
        self.logic_board.check_end()
        self.logic_board.advanced_move(self, move, additional_info)
        self.logic_board.update_history()

    def new_piece_position(self, event):
        last_mouse_position = event.lastScenePos()
        new_mouse_position = event.scenePos()
        last_piece_position = self.scenePos()

        new_x = new_mouse_position.x() - last_mouse_position.x() + last_piece_position.x()
        new_y = new_mouse_position.y() - last_mouse_position.y() + last_piece_position.y()
        return QPointF(new_x, new_y)

    def graphic_move(self, field):
        self.last_field = self.current_field
        self.current_field = field
        self.set_in_field(field)
        self.graphic_board.clear_captures()
        self.graphic_board.clear_circles()

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
