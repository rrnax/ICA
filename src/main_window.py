from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QPushButton, QGraphicsScene, QGraphicsView, QVBoxLayout
from PyQt5.QtGui import QColor, QIcon, QCursor
from engine_frame import EngineFrame
from moves_options_widget import MovesOptionsList
from menu_widget import MenuWidget

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class MainWindow(QMainWindow):

    def __init__(self):
        # Window settings
        super().__init__()

        self.moves_frame = MovesOptionsList(self)

        self.setWindowTitle("Interactive Chess assistant")
        self.setMinimumSize(QSize(1200, 820))
        self.setStyleSheet(f"background-color: {color_theme[0]};")

        self.game_frame = QFrame(self)
        self.game_frame.setGeometry(0, 0, 750, 550)

        self.stats_frame = QFrame(self)
        self.stats_frame.setGeometry(750, 0, 450, 550)
        self.stats_frame.setStyleSheet(f"border-left: 1px solid {color_theme[3]};")

        self.engine_frame = EngineFrame(self)

        game_scene = QGraphicsScene()
        self.game_view = QGraphicsView(game_scene, self.game_frame)
        self.game_view.setStyleSheet(f"border: none")
        self.game_view.setBackgroundBrush(QColor(0, 0, 0))

        self.menu_btn = QPushButton(self)
        self.menu_btn.setIcon(QIcon('../resources/menu.png'))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.menu_btn.setGeometry(10, 10, 50, 50)
        self.menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_theme[1]};
                border: 2px solid {color_theme[3]};
                border-radius: 5px;
            }}
            
            QPushButton:hover {{
                background-color: {color_theme[3]};
            }}
        """)

        btn1= QPushButton("Zamknij")

        self.menu_layout = QVBoxLayout()
        self.menu_layout.addWidget(btn1)

        self.menu_widget = QWidget(self)
        self.menu_widget.setGeometry(-400, 100, 400, 800)
        self.menu_widget.setStyleSheet(f"background-color: {color_theme[1]};")
        self.menu_widget.setLayout(self.menu_layout)

        self.menu_btn.clicked.connect(self.open_menu)
        btn1.clicked.connect(self.close_menu)
    def resizeEvent(self, event):
        self.upadte_sizes()

    def upadte_sizes(self):
        self.game_frame.resize((self.size().width() - 1200) + 750, (self.size().height() - 820) + 550)
        self.game_view.setGeometry(self.game_frame.rect())
        self.stats_frame.setGeometry((self.size().width() - 1200) + 750, 0, 450, (self.size().height() - 820) + 550)
        self.moves_frame.update_size(self.size())
        self.engine_frame.update_size(self.size())

    def open_menu(self):
        self.menu_widget.animation = QPropertyAnimation(self.menu_widget, b"geometry", self.menu_widget)
        self.menu_widget.animation.setDuration(1000)
        self.menu_widget.animation.setStartValue(QRect(-400, 100, 400, 800))
        self.menu_widget.animation.setEndValue(QRect(0, 100, 400, 800))
        self.menu_widget.animation.start()

    def close_menu(self):
        self.menu_widget.animation = QPropertyAnimation(self.menu_widget, b"geometry", self.menu_widget)
        self.menu_widget.animation.setDuration(1000)
        self.menu_widget.animation.setStartValue(QRect(0, 100, 400, 800))
        self.menu_widget.animation.setEndValue(QRect(-400, 100, 400, 800))
        self.menu_widget.animation.start()