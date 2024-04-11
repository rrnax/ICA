from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt


class Loader(QLabel):
    def __init__(self, path):
        super().__init__()
        self.setFixedSize(100, 100)
        self.setScaledContents(True)
        self.movie = QMovie(path)
        self.setMovie(self.movie)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()