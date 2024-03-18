import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("../resources/PoetsenOne-Regular.ttf")
if font_id != -1:
    app.setFont(QFont("Poetsen One"))
main_window = MainWindow()
main_window.show()
app.exec()
