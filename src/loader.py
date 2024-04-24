from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMovie
from sheard_memory import SharedMemoryStorage


class Loader(QLabel):
    def __init__(self, path):
        super().__init__()
        self.storage = SharedMemoryStorage()

        self.setFixedSize(150, 200)
        self.setStyleSheet(f"background-color: {self.storage.color_theme[1]};")
        self.setScaledContents(True)

        self.movie = QMovie(path)
        self.setMovie(self.movie)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()

    def update_style(self):
        self.setStyleSheet(f"background-color: {self.storage.color_theme[1]};")
