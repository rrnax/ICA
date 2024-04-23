import sys
import os
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt

script_name = sys.argv[0]
full_path = os.path.abspath(script_name)
work_dir = os.path.dirname(full_path)
os.chdir(work_dir)
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
font_id = QFontDatabase.addApplicationFont("../resources/PoetsenOne-Regular.ttf")
if font_id != -1:
    app.setFont(QFont("Poetsen One"))
main_window = MainWindow()
main_window.show()
app.exec()
