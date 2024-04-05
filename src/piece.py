from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem
from logic_board import LogicBoard

# Here are contribution license links fo images
# <a href="https://www.flaticon.com/free-icons/chess-piece" title="chess piece icons">Chess piece icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by deemakdaksina - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by Stockio - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by SBTS2018 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/tactic" title="tactic icons">Tactic icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/bishop" title="bishop icons">Bishop icons created by Victoruler - Flaticon</a>

# Position highlighting colors
highlight = ["#a9aba7"]


class VirtualPiece(QGraphicsPixmapItem):
    def __init__(self, name, value, field):
        super().__init__()
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
        self.logic_board.graphic_board.find_legal_fields(self.legal_moves)
        if self.logic_board.check_turn() == self.name[0]:
            self.setCursor(Qt.ClosedHandCursor)
            # self.field.setBrush(QColor(highlight[0]))

    def mouseDoubleClickEvent(self, event):
        pass
        # if self.logic_board.check_turn() == self.name[0]:
            # self.field.setBrush(self.field.orginal_brush)

    def mouseMoveEvent(self, event):
        if self.logic_board.check_turn() == self.name[0]:
            self.setPos(self.calc_position(event))

    def mouseReleaseEvent(self, event):
        # Check position on board or outside
        if self.logic_board.check_turn() == self.name[0]:
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

                            # Start move validation

                            print(self.legal_moves)
                            # End move validation

                            # Place piece on correct field
                            x = (field.rect().x() +
                                 (field.rect().width() -
                                  self.image.width()) /
                                 2.0)
                            y = (field.rect().y() +
                                 (field.rect().height() -
                                  self.image.height()) /
                                 2.0)

                            # if self.lastPos.x() != x and self.lastPos.y() != y:
                            #     self.field.setBrush(self.field.orginal_brush)

                            self.logic_board.push_uci(self.field.chess_pos + field.chess_pos)
                            self.setPos(x, y)
                            self.field = field
                            self.lastPos = QPointF(x, y)
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



