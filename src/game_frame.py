from PyQt5.QtWidgets import QFrame, QGraphicsView, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor, QPainter, QPixmap, QPen
from PyQt5.QtCore import Qt
from chess_board import ChessBoard
from side_dialog import SideDialog
from message_dialog import MessageDialog
from sheard_memory import SharedMemoryStorage


class GameFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = SharedMemoryStorage()

        # Containers creation
        self.game_scene = ChessBoard(self, logic=self.parent().logic_board)
        self.game_view = QGraphicsView(self.game_scene, self)
        self.set_properties()
        self.no_frame = self.create_style()
        self.setStyleSheet(self.no_frame)

    def set_properties(self):
        # This container
        self.setGeometry(0, 0, 750, 550)

        # Items
        self.game_view.setRenderHint(QPainter.Antialiasing)
        self.game_view.setFixedSize(750, 550)
        self.game_view.setBackgroundBrush(QColor(self.storage.color_theme[0]))
        self.game_view.setObjectName("game-frame")

    def update_size(self, new_size):
        self.setGeometry(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_view.setFixedSize((new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.setSceneRect(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.draw_board((new_size.height() - 820) + 490)
        self.game_scene.resize_pieces()

    # Occasionally dialogs
    def side_up(self):
        side_dialog = SideDialog(self, logic=self.parent().logic_board)
        side_dialog.exec()

    def winner_up(self, widget):
        message_dialog = MessageDialog(content=widget)
        message_dialog.exec()

    def make_winner_msg(self, winner):
        pixmap = QPixmap("../resources/pieces/" + winner + ".png")
        pixmap = pixmap.scaled(100, 100, transformMode=Qt.SmoothTransformation)
        image = QLabel()
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)
        print(winner)

        label = None
        if "king" in winner:
            if winner == "w_king":
                label = QLabel("Wygrały Białe!")
            elif winner == "b_king":
                label = QLabel("Wygrały Czarne!")
        else:
            label = QLabel("Remis!")
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(160, 20)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.addWidget(label)
        layout.addWidget(image)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def create_style(self):
        return f"""
            #game-frame {{
                border: none;
            }}
        """

    def update_theme(self):
        self.game_view.setBackgroundBrush(QColor(self.storage.color_theme[0]))
        for field in self.game_scene.fields:
            field.field_labels[0].setDefaultTextColor(QColor(self.storage.color_theme[3]))
            field.field_labels[1].setDefaultTextColor(QColor(self.storage.color_theme[3]))
            if self.storage.color_theme[0] == "#1E1F22":
                pen = QPen(Qt.NoPen)
                field.setPen(pen)
            else:
                pen = QPen(QColor(self.storage.color_theme[3]))
                field.setPen(pen)


