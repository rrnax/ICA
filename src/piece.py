from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem

# <a href="https://www.flaticon.com/free-icons/chess-piece" title="chess piece icons">Chess piece icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by deemakdaksina - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by Stockio - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by SBTS2018 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/tactic" title="tactic icons">Tactic icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/bishop" title="bishop icons">Bishop icons created by Victoruler - Flaticon</a>


class VirtualPiece(QGraphicsPixmapItem):
    def __init__(self, name, value, field):
        super().__init__()

        self.name = name
        self.fen_id = value
        self.field = field
        self.image = None
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
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        pass

    def mouseMoveEvent(self, event):
        self.setPos(self.calc_position(event))

    def mouseReleaseEvent(self, event):
        chess_board = self.scene().parent().game_scene
        new_pos = self.calc_position(event)
        if ((new_pos.x() + self.image.width()/2 >= chess_board.board_x + chess_board.board_length
             or new_pos.y() + self.image.height()/2 >= chess_board.board_y + chess_board.board_length)
                or (new_pos.x() + self.image.width()/2 <= chess_board.board_x
                    or new_pos.y() + self.image.height()/2 <= chess_board.board_y)):
            self.setPos(self.lastPos)
        else:
            for field in chess_board.fields:
                start_pos = QPointF(field.graphic_pos.rect().x(),
                                    field.graphic_pos.rect().y())
                end_pos = QPointF(field.graphic_pos.rect().x() +
                                  field.graphic_pos.rect().width(),
                                  field.graphic_pos.rect().y() +
                                  field.graphic_pos.rect().height())

                if ((start_pos.x() <= new_pos.x() + self.image.width()/2 <= end_pos.x())
                        and (start_pos.y() <= new_pos.y() + self.image.height()/2 <= end_pos.y())):
                    x = (field.graphic_pos.rect().x() +
                         (field.graphic_pos.rect().width() -
                          self.image.width()) /
                         2.0)
                    y = (field.graphic_pos.rect().y() +
                         (field.graphic_pos.rect().height() -
                          self.image.height()) /
                         2.0)
                    ###Move validation

                    ###
                    self.setPos(x, y)
                    self.field = field
                    self.lastPos = QPointF(x, y)

        self.setCursor(Qt.OpenHandCursor)

    def calc_position(self, event):
        last_cursor_pos = event.lastScenePos()
        new_cursor_pos = event.scenePos()
        piece_pos = self.scenePos()

        new_x = new_cursor_pos.x() - last_cursor_pos.x() + piece_pos.x()
        new_y = new_cursor_pos.y() - last_cursor_pos.y() + piece_pos.y()
        return QPointF(new_x, new_y)

    def highlight_fields(self):
        if self.field.brushed:
            self.field.graphic_pos.setBrush(self.field.orginal_brush)
            self.field.brushed = False
        else:
            self.field.graphic_pos.setBrush(QColor("#4ecbf5"))
            self.field.brushed = True
