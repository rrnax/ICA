from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize
from QSwitchControl import SwitchControl
from logic_board import LogicBoard
from save_dialog import SaveDialog
from load_dialog import LoadDialog
from openings_dialog import OpeningsDialog
from endings_dialog import EndingDialog
from sheard_memory import SharedMemoryStorage


class MenuSlideFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic_board = self.parent().logic_board
        self.storage = SharedMemoryStorage()

        # Init elements
        self.opening_dialog = OpeningsDialog(self)
        self.ending_dialog = EndingDialog(self)
        self.load_dialog = LoadDialog(self)
        self.save_dialog = SaveDialog(self)

        self.app_label = QLabel()
        self.space_block = QLabel()
        self.new_game_btn = QPushButton("Gra")
        self.analyze_btn = QPushButton("Analiza")
        self.openings_btn = QPushButton("Otwarcia")
        self.endings_btn = QPushButton("Końcówki")
        self.load_btn = QPushButton("Wczytaj")
        self.save_btn = QPushButton("Zapisz")
        self.hide_btn = QPushButton("Powrót")
        self.moon = QLabel()
        self.switch = SwitchControl(bg_color=self.storage.color_theme[3], active_color=self.storage.color_theme[1], change_cursor=True)
        self.sun = QLabel()
        self.theme_mode = QWidget()
        self.menu_style = self.create_style()
        self.animation = QPropertyAnimation(self, b"geometry", self)

        # Creating widget
        self.set_items_properties()
        self.set_layouts()
        self.set_general_properties()
        self.setStyleSheet(self.menu_style)
        self.assign_actions()

    # Connecting elements with actions
    def assign_actions(self):
        self.new_game_btn.clicked.connect(self.open_game)
        self.analyze_btn.clicked.connect(self.open_analyze)
        self.hide_btn.clicked.connect(self.close_menu)
        self.save_btn.clicked.connect(self.open_saving)
        self.load_btn.clicked.connect(self.open_loading)
        self.openings_btn.clicked.connect(self.open_openings)
        self.endings_btn.clicked.connect(self.open_endings)
        self.switch.stateChanged.connect(self.parent().change_theme)

    # Widget properties
    def set_general_properties(self):
        self.setGeometry(-300, 0, 300, 820)
        self.setObjectName("menu-slide-frame")

    # All items properties
    def set_items_properties(self):
        # Trademark
        app_logo = QPixmap("../resources/appmark.png")
        self.app_label.setFixedSize(300, 200)
        self.app_label.setPixmap(app_logo)
        self.app_label.setScaledContents(True)

        self.space_block.setFixedSize(300, 20)

        # Game mode button
        self.new_game_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.new_game_btn.setIcon(QIcon("../resources/mini-board.png"))
        self.new_game_btn.setIconSize(QSize(80, 40))
        self.new_game_btn.setObjectName("new-game-btn")

        # Analyze mode button
        self.analyze_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.analyze_btn.setIcon(QIcon("../resources/loupe.png"))
        self.analyze_btn.setIconSize(QSize(80, 40))
        self.analyze_btn.setObjectName("analyze-btn")
        
        # Openings section button
        self.openings_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.openings_btn.setIcon(QIcon("../resources/opens.png"))
        self.openings_btn.setIconSize(QSize(80, 40))
        self.openings_btn.setObjectName("openings-btn")

        # Endings section button
        self.endings_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.endings_btn.setIcon(QIcon("../resources/ends.png"))
        self.endings_btn.setIconSize(QSize(80, 40))
        self.endings_btn.setObjectName("endings-btn")

        # Load game or position on board
        self.load_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.load_btn.setIcon(QIcon("../resources/load_game.png"))
        self.load_btn.setIconSize(QSize(80, 40))
        self.load_btn.setObjectName("load-btn")
        
        # Save position or board
        self.save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.save_btn.setIcon(QIcon("../resources/saves.png"))
        self.save_btn.setIconSize(QSize(80, 40))
        self.save_btn.setObjectName("save-btn")

        # Hide menu button
        self.hide_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.hide_btn.setIcon(QIcon("../resources/back_arrow.png"))
        self.hide_btn.setIconSize(QSize(80, 40))
        self.hide_btn.setObjectName("hide-btn")

        # Images to switch and switch to change theme
        moon_pixmap = QPixmap("../resources/moon.png")
        moon_pixmap = moon_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.moon.setPixmap(moon_pixmap)
        sun_pixmap = QPixmap("../resources/sun.png")
        sun_pixmap = sun_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.sun.setPixmap(sun_pixmap)

        # Theme widget
        self.theme_mode.setFixedSize(300, 80)

    # Connecting widget with layouts and items
    def set_layouts(self):
        # Theme mode layout
        theme_mode_layout = QHBoxLayout()
        theme_mode_layout.setAlignment(Qt.AlignCenter)
        theme_mode_layout.addWidget(self.moon)
        theme_mode_layout.addWidget(self.switch)
        theme_mode_layout.addWidget(self.sun)
        self.theme_mode.setLayout(theme_mode_layout)

        # Menu layout
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(20)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.addWidget(self.app_label)
        menu_layout.addWidget(self.new_game_btn)
        menu_layout.addWidget(self.analyze_btn)
        menu_layout.addWidget(self.openings_btn)
        menu_layout.addWidget(self.endings_btn)
        menu_layout.addWidget(self.load_btn)
        menu_layout.addWidget(self.save_btn)
        menu_layout.addWidget(self.hide_btn)
        menu_layout.addWidget(self.theme_mode)
        self.setLayout(menu_layout)

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

    # Actions on buttons
    def open_game(self):
        self.logic_board.sets_game("game")
        self.close_menu()

    def open_analyze(self):
        self.logic_board.sets_game("analyze")
        self.close_menu()

    def open_saving(self):
        pgn = self.logic_board.create_pgn()
        self.save_dialog.load_fen(actual_FEN=self.logic_board.fen())
        self.save_dialog.load_pgn(actual_PGN=pgn)
        self.save_dialog.exec()

    def open_loading(self):
        self.load_dialog.exec()

    def open_endings(self):
        self.ending_dialog.exec()

    def open_openings(self):
        self.opening_dialog.exec()

    def veify_state(self):
        if self.switch.checkState() == 2:
            return True
        else:
            return False

    # Making style for container and updating it
    def create_style(self):
        return f"""
            #menu-slide-frame {{
                background-color: {self.storage.color_theme[0]};
                border-right: none; 
            }}

            #new-game-btn, #analyze-btn, #openings-btn, #endings-btn, #load-btn, #save-btn, #hide-btn {{
                width: 300px;
                height: 50px;
                padding-left: 20px;
                background-color: {self.storage.color_theme[0]};
                color: {self.storage.color_theme[3]};
                font-size: 30px;
                text-align: left;
                border: none;
            }}

            #new-game-btn:hover, #analyze-btn:hover, #openings-btn:hover, #endings-btn:hover, #load-btn:hover, 
            #save-btn:hover, #hide-btn:hover {{ background-color: {self.storage.color_theme[3]};
                color: {self.storage.color_theme[0]};
            }}
        """

    def update_style(self):
        style = self.create_style()
        self.setStyleSheet(style)
        app_logo = QPixmap("../resources/appmark_gray.png")
        self.app_label.setPixmap(app_logo)
        self.opening_dialog.update_style()
        self.ending_dialog.update_style()
        self.load_dialog.update_style()
        self.save_dialog.update_style()

    def load_board(self, notation, content):
        if notation == "pgn":
            self.logic_board.load_position_pgn(game=content)
        elif notation == "fen":
            self.logic_board.load_position_fen(fen=content)

# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/insight" title="insight icons">Insight icons created by Awicon - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/open-door" title="open door icons">Open door icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/final" title="final icons">Final icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/loading" title="loading icons">Loading icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/save" title="save icons">Save icons created by Aldo Cervantes - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/back-arrow" title="back arrow icons">Back arrow icons created by Vector Squad - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/night" title="night icons">Night icons created by kmg design - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/self.sun" title="self.sun icons">self.sun icons created by Freepik - Flaticon</a>