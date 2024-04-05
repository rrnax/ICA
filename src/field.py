from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QFont, QColor
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


# Virtual representation of chess board field
class VirtualField(QGraphicsRectItem):
    def __init__(self, chess_pos):
        super().__init__()

        self.chess_pos = chess_pos
        self.orginal_brush = None
        self.field_labels = [QGraphicsTextItem(chess_pos[1]), QGraphicsTextItem(chess_pos[0].upper())]
        self.unmounted = True
        self.brushed = False
        pen = QPen(Qt.NoPen)
        self.setPen(pen)

        # Set labels for edge fields
        font = QFont()
        font.setPointSize(18)
        for label in self.field_labels:
            label.setFont(font)
            label.setDefaultTextColor(QColor(color_theme[3]))