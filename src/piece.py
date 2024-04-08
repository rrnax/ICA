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
    def __init__(self, name, value, field):
        super().__init__()
        self.setZValue(3)
        self.logic_board = LogicBoard()

        self.name = name
        self.fen_id = value
        self.field = field
        self.image = None
        self.legal_moves = None
        self.set_image()

        if self.image is not None:
            self.setPixmap(self.image)

        self.setAcceptHoverEvents(True)
        self.lastPos = None
        self.captured_pos = None

    def set_image(self):
        path = "../resources/pieces/" + self.name + ".png"
        self.image = QPixmap(path)

    def set_position(self, x, y):
        self.setPos(x, y)
        self.lastPos = QPointF(x, y)

    def update_pixmap(self, pixmap):
        if pixmap is not None:
            self.setPixmap(pixmap)

    def hoverEnterEvent(self, event):
        if self.logic_board.check_turn() == self.name[0]:
            self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        self.legal_moves = self.logic_board.piece_moves(self.field.chess_pos)
        if self.logic_board.check_turn() == self.name[0] and self.logic_board.ended_game is None:
            self.logic_board.graphic_board.highlight_field(self.field)
            self.logic_board.graphic_board.find_legal_fields(self.legal_moves)
            self.setCursor(Qt.ClosedHandCursor)

    def mouseDoubleClickEvent(self, event):
        if self.logic_board.check_turn() == self.name[0] and self.logic_board.ended_game is None:
            self.logic_board.graphic_board.clear_circles()
            self.logic_board.graphic_board.clear_captures()

    def mouseMoveEvent(self, event):
        if self.logic_board.check_turn() == self.name[0] and self.logic_board.ended_game is None:
            self.setPos(self.calc_position(event))

    def mouseReleaseEvent(self, event):
        # Check position on board or outside
        if self.logic_board.check_turn() == self.name[0] and self.logic_board.ended_game is None:
            chess_board = self.logic_board.graphic_board
            new_pos = self.calc_position(event)
            if ((new_pos.x() + self.image.width()/2 >= chess_board.board_x + chess_board.board_length
                 or new_pos.y() + self.image.height()/2 >= chess_board.board_y + chess_board.board_length)
                    or (new_pos.x() + self.image.width()/2 <= chess_board.board_x
                        or new_pos.y() + self.image.height()/2 <= chess_board.board_y)):
                self.setPos(self.lastPos)
            else:
                # Check position for field on board
                for field in chess_board.fields:
                    if field.chess_pos in self.legal_moves:
                        start_pos = QPointF(field.rect().x(),
                                            field.rect().y())
                        end_pos = QPointF(field.rect().x() +
                                          field.rect().width(),
                                          field.rect().y() +
                                          field.rect().height())

                        if ((start_pos.x() <= new_pos.x() + self.image.width()/2 <= end_pos.x())
                                and (start_pos.y() <= new_pos.y() + self.image.height()/2 <= end_pos.y())):

                            move = Move.from_uci(self.field.chess_pos + field.chess_pos)

                            if self.logic_board.is_capture(move):
                                chess_board.find_capture_piece(field.chess_pos)
                            if self.fen_id != 'K' and self.fen_id != 'k':
                                self.logic_board.graphic_board.clear_check()
                            self.logic_board.graphic_board.check_castling(move)
                            self.logic_board.graphic_board.clear_circles()
                            self.logic_board.graphic_board.clear_captures()

                            # Place piece on correct field
                            x = (field.rect().x() +
                                 (field.rect().width() -
                                  self.image.width()) /
                                 2.0)
                            y = (field.rect().y() +
                                 (field.rect().height() -
                                  self.image.height()) /
                                 2.0)

                            add_info = self.logic_board.find_info(move)

                            self.logic_board.push(move)
                            self.setPos(x, y)
                            self.field = field
                            self.lastPos = QPointF(x, y)
                            chess_board.legal_moves = None
                            self.logic_board.graphic_board.find_check()
                            self.logic_board.check_end()
                            self.logic_board.advanced_move(self, move, add_info)

                            self.logic_board.stats_frame.update_history()

                    else:
                        self.setPos(self.lastPos)

            self.setCursor(Qt.OpenHandCursor)

    def calc_position(self, event):
        last_cursor_pos = event.lastScenePos()
        new_cursor_pos = event.scenePos()
        piece_pos = self.scenePos()

        new_x = new_cursor_pos.x() - last_cursor_pos.x() + piece_pos.x()
        new_y = new_cursor_pos.y() - last_cursor_pos.y() + piece_pos.y()
        return QPointF(new_x, new_y)

    def graphic_move(self, target_field):
        for field in self.logic_board.graphic_board.fields:
            if field.chess_pos == target_field:
                x = (field.rect().x() +
                     (field.rect().width() -
                      self.image.width()) /
                     2.0)
                y = (field.rect().y() +
                     (field.rect().height() -
                      self.image.height()) /
                     2.0)
                self.setPos(x, y)
                self.field = field
                self.lastPos = QPointF(x, y)
                self.logic_board.graphic_board.legal_moves = None
