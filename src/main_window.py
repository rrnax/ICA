import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor

color_theme = ["#191A19", "#1E5128", "#4E9F3D", "#D8E9A8", "#FFFFFF"]


class MainWindow(QMainWindow):

    def __init__(self):
        # Window settings
        super().__init__()
        self.setWindowTitle("Interactive Chess assistant")
        self.setMinimumSize(QSize(1200, 820))
        self.setStyleSheet(f"background-color: {color_theme[0]};")

        general_widget = QWidget()

        self.game_frame = QFrame(self)
        self.game_frame.setGeometry(0, 0, 750, 550)
        # self.game_frame.setStyleSheet("QFrame { border-radius: 100px; border: 2px solid blue; }")

        self.stats_frame = QFrame(self)
        self.stats_frame.setGeometry(750, 0, 450, 550)
        self.stats_frame.setStyleSheet(f"border-left: 1px solid {color_theme[3]};")

        self.engine_frame = QFrame(self)
        self.engine_frame.setGeometry(0, 550, 1200, 70)
        self.engine_frame.setStyleSheet(f"border-top: 1px solid {color_theme[3]}; border-bottom: 1px solid {color_theme[3]};")

        engine_label = QLabel("Engine: Stockfish")
        depth_label = QLabel("Depth: 20")
        moves_filter_button = QToolButton()
        moves_filter_button.setStyleSheet(f"border: 1px solid {color_theme[3]}; border-radius: 10px;")
        moves_filter_button.setFixedSize(100, 50)
        moves_filter_button.setText("Filters")
        engine_settings_button = QPushButton("Settings")
        engine_settings_button.setStyleSheet(f" border: 1px solid {color_theme[3]}; border-radius: 10px;")
        engine_settings_button.setFixedSize(100, 50)

        self.engine_frame_layout = QHBoxLayout()
        self.engine_frame_layout.setSpacing(400)
        left_widget = QWidget()
        left_widget.setStyleSheet(f"border: none; color: {color_theme[3]}; font-size: 20px;")
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(20, 0, 0, 0)
        left_layout.addWidget(engine_label)
        left_layout.addWidget(depth_label)
        left_widget.setLayout(left_layout)
        self.engine_frame_layout.addWidget(left_widget)
        right_widget = QWidget()
        right_widget.setStyleSheet(f"border: none;color: {color_theme[3]}; font-size: 20px;")
        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(moves_filter_button)
        right_layout.addWidget(engine_settings_button)
        right_widget.setLayout(right_layout)
        self.engine_frame_layout.addWidget(right_widget)
        self.engine_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.engine_frame.setLayout(self.engine_frame_layout)

        game_scene = QGraphicsScene()
        self.game_view = QGraphicsView(game_scene, self.game_frame)
        self.game_view.setStyleSheet(f"border: none")
        self.game_view.setBackgroundBrush(QColor(0, 0, 0))

        self.moves_frame = QListWidget(self)
        self.moves_frame.setGeometry(0, 620, 1200, 200)
        self.moves_frame.setStyleSheet(f"border: none;")


    def resizeEvent(self, event):
        self.upadte_sizes()

    def upadte_sizes(self):
        text = f"SZ: {self.size().width()} W: {self.size().height()}"
        self.game_frame.resize((self.size().width() - 1200) + 750, (self.size().height() - 820) + 550)
        self.game_view.setGeometry(self.game_frame.rect())
        self.engine_frame_layout.setSpacing(400 + self.size().width()-1200)
        self.stats_frame.setGeometry((self.size().width() - 1200) + 750, 0, 450, (self.size().height() - 820) + 550)
        self.engine_frame.setGeometry(0, (self.size().height() - 820) + 550, (self.size().width() - 1200) + 1200, 70)
        self.moves_frame.setGeometry(0, (self.size().height() - 820) + 620, (self.size().width() - 1200) + 1200, 200)



app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec_())
