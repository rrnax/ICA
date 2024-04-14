from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize
from QSwitchControl import SwitchControl
from logic_board import LogicBoard
from save_dialog import SaveDialog
from load_dialog import LoadDialog
from openings_dialog import OpeningsDialog
from endings_dialog import EndingDialog
from sheard_memory import color_theme, color_theme_light, color_theme_dark

# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/insight" title="insight icons">Insight icons created by Awicon - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/open-door" title="open door icons">Open door icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/final" title="final icons">Final icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/loading" title="loading icons">Loading icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/save" title="save icons">Save icons created by Aldo Cervantes - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/back-arrow" title="back arrow icons">Back arrow icons created by Vector Squad - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/night" title="night icons">Night icons created by kmg design - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/sun" title="sun icons">Sun icons created by Freepik - Flaticon</a>


class MenuSlideFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic_board = LogicBoard()

        # Layout elements
        app_logo = QPixmap("../resources/appmark.png")
        app_label = QLabel()
        app_label.setFixedSize(300, 200)
        app_label.setPixmap(app_logo)
        app_label.setScaledContents(True)

        space_block = QLabel()
        space_block.setFixedSize(300, 20)

        new_game_btn = QPushButton("Gra")
        new_game_btn.setCursor(QCursor(Qt.PointingHandCursor))
        new_game_btn.setIcon(QIcon("../resources/mini-board.png"))
        new_game_btn.setIconSize(QSize(80, 40))

        analyze_btn = QPushButton("Analiza")
        analyze_btn.setCursor(QCursor(Qt.PointingHandCursor))
        analyze_btn.setIcon(QIcon("../resources/loupe.png"))
        analyze_btn.setIconSize(QSize(80, 40))

        openings_btn = QPushButton("Otwarcia")
        openings_btn.setCursor(QCursor(Qt.PointingHandCursor))
        openings_btn.setIcon(QIcon("../resources/opens.png"))
        openings_btn.setIconSize(QSize(80, 40))

        endings_btn = QPushButton("Końcówki")
        endings_btn.setCursor(QCursor(Qt.PointingHandCursor))
        endings_btn.setIcon(QIcon("../resources/ends.png"))
        endings_btn.setIconSize(QSize(80, 40))

        load_btn = QPushButton("Wczytaj")
        load_btn.setCursor(QCursor(Qt.PointingHandCursor))
        load_btn.setIcon(QIcon("../resources/load_game.png"))
        load_btn.setIconSize(QSize(80, 40))

        save_btn = QPushButton("Zapisz")
        save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        save_btn.setIcon(QIcon("../resources/saves.png"))
        save_btn.setIconSize(QSize(80, 40))

        hide_btn = QPushButton("Powrót")
        hide_btn.setCursor(QCursor(Qt.PointingHandCursor))
        hide_btn.setIcon(QIcon("../resources/back_arrow.png"))
        hide_btn.setIconSize(QSize(80, 40))

        moon = QLabel()
        moon_pixmap = QPixmap("../resources/moon.png")
        moon_pixmap = moon_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        moon.setPixmap(moon_pixmap)

        self.switch = SwitchControl(bg_color=color_theme[1], active_color=color_theme[3], change_cursor=True)

        sun = QLabel()
        sun_pixmap = QPixmap("../resources/sun.png")
        sun_pixmap = sun_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        sun.setPixmap(sun_pixmap)

        theme_mode_layout = QHBoxLayout()
        theme_mode_layout.setAlignment(Qt.AlignCenter)
        theme_mode_layout.addWidget(moon)
        theme_mode_layout.addWidget(self.switch)
        theme_mode_layout.addWidget(sun)

        theme_mode = QWidget()
        theme_mode.setFixedSize(300, 80)
        theme_mode.setLayout(theme_mode_layout)
        # switch.setStyleSheet(f"background-color: {color_theme[3]}")
        # switch.setAnimation(True)
        # switch.setCircleDiameter(30)

        # Layout sets
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(20)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.addWidget(app_label)
        menu_layout.addWidget(new_game_btn)
        menu_layout.addWidget(analyze_btn)
        menu_layout.addWidget(openings_btn)
        menu_layout.addWidget(endings_btn)
        menu_layout.addWidget(load_btn)
        menu_layout.addWidget(save_btn)
        menu_layout.addWidget(hide_btn)
        menu_layout.addWidget(theme_mode)

        # General sets for menu
        self.animation = QPropertyAnimation(self, b"geometry", self)
        self.setGeometry(-300, 0, 300, 820)
        self.setLayout(menu_layout)
        self.setObjectName("menu-slide-frame")
        self.css = f"""
        #menu-slide-frame {{
            background-color: {color_theme[0]};
            border-right: none; 
        }}
        
        QPushButton {{
            width: 300px;
            height: 50px;
            padding-left: 20px;
            background-color: {color_theme[0]};
            color: {color_theme[3]};
            font-size: 30px;
            text-align: left;
            border: none;
        }}
        
        QPushButton:hover {{
            background-color: {color_theme[3]};
            color: {color_theme[0]};
        }}
        """
        self.setStyleSheet(self.css)

        # Actions
        new_game_btn.clicked.connect(self.open_game)
        analyze_btn.clicked.connect(self.open_analyze)
        hide_btn.clicked.connect(self.close_menu)
        save_btn.clicked.connect(self.open_saving)
        load_btn.clicked.connect(self.open_loading)
        openings_btn.clicked.connect(self.open_openings)
        endings_btn.clicked.connect(self.open_endings)
        self.switch.stateChanged.connect(self.change_theme)

    # Show or hide menu
    def open_menu(self):
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(-300, 0, 300, 820))
        self.animation.setEndValue(QRect(0, 0, 300, 820))
        self.animation.start()

    def close_menu(self):
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(0, 0, 300, 820))
        self.animation.setEndValue(QRect(-300, 0, 300, 820))
        self.animation.start()

    # For window change
    def update_size(self, new_size):
        self.setFixedSize(300, (new_size.height() - 820) + 820)

    def open_game(self):
        self.logic_board.sets_game("game")
        self.close_menu()

    def open_analyze(self):
        self.logic_board.sets_game("analyze")
        self.close_menu()

    def open_saving(self):
        save_dialog = SaveDialog()
        save_dialog.exec()

    def open_loading(self):
        load_dialog = LoadDialog()
        load_dialog.exec()

    def open_endings(self):
        ending_dialog = EndingDialog()
        ending_dialog.exec()

    def open_openings(self):
        opening_dialog = OpeningsDialog()
        opening_dialog.exec()

    def change_theme(self):
        if self.switch.checkState() == 2:
            color_theme = color_theme_light
        else:
            color_theme = color_theme_dark

        self.css = f"""
                #menu-slide-frame {{
                    background-color: {color_theme[0]};
                    border-right: none; 
                }}

                QPushButton {{
                    width: 300px;
                    height: 50px;
                    padding-left: 20px;
                    background-color: {color_theme[0]};
                    color: {color_theme[3]};
                    font-size: 30px;
                    text-align: left;
                    border: none;
                }}

                QPushButton:hover {{
                    background-color: {color_theme[3]};
                    color: {color_theme[0]};
                }}
                """

        self.setStyleSheet(self.css)
        self.repaint()


