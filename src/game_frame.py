from PyQt5.QtWidgets import QFrame, QGraphicsView, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtCore import Qt
from chess_board import ChessBoard
from side_dialog import SideDialog
from message_dialog import MessageDialog

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class GameFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 750, 550)
        self.setStyleSheet(f"""
                    #game-frame {{
                        border: none;
                    }}
                """)

        self.game_scene = ChessBoard(self)
        self.game_view = QGraphicsView(self.game_scene, self)
        self.game_view.setRenderHint(QPainter.Antialiasing)
        self.game_view.setFixedSize(750, 550)
        self.game_view.setBackgroundBrush(QColor(color_theme[0]))
        self.game_view.setObjectName("game-frame")

    def update_size(self, new_size):
        self.setGeometry(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_view.setFixedSize((new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.setSceneRect(0, 0, (new_size.width() - 1200) + 750, (new_size.height() - 820) + 550)
        self.game_scene.draw_board((new_size.height() - 820) + 490)
        self.game_scene.resize_pieces()

    def side_up(self):
        side_dialog = SideDialog()
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
