from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]
# <a href="https://www.flaticon.com/free-icons/chess" title="chess icons">Chess icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/insight" title="insight icons">Insight icons created by Awicon - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/open-door" title="open door icons">Open door icons created by rizal2109 - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/final" title="final icons">Final icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/loading" title="loading icons">Loading icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/save" title="save icons">Save icons created by Aldo Cervantes - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/back-arrow" title="back arrow icons">Back arrow icons created by Vector Squad - Flaticon</a>


class MenuSlideFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout elements
        app_logo = QPixmap("../resources/appmark.png")
        app_label = QLabel()
        app_label.setFixedSize(300, 200)
        app_label.setPixmap(app_logo)
        app_label.setScaledContents(True)

        space_block = QLabel()
        space_block.setFixedSize(400, 20)

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

        # Layout sets
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(20)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.addWidget(app_label)
        menu_layout.addWidget(space_block)
        menu_layout.addWidget(new_game_btn)
        menu_layout.addWidget(analyze_btn)
        menu_layout.addWidget(openings_btn)
        menu_layout.addWidget(endings_btn)
        menu_layout.addWidget(load_btn)
        menu_layout.addWidget(save_btn)
        menu_layout.addWidget(hide_btn)

        # General sets for menu
        self.animation = QPropertyAnimation(self, b"geometry", self)
        self.setGeometry(-300, 0, 300, 820)
        self.setLayout(menu_layout)
        self.setObjectName("menu-slide-frame")
        self.setStyleSheet(f"""
        #menu-slide-frame {{
            background-color: {color_theme[0]};
            border-right: 1px solid {color_theme[3]}; 
        }}
        
        QPushButton {{
            width: 300px;
            height: 50px;
            padding-left: 20px;
            background-color: transparent;
            color: {color_theme[4]};
            font-size: 30px;
            text-align: left;
        }}
        
        QPushButton:hover {{
            background-color: {color_theme[3]};
            color: {color_theme[0]};
        }}
        """)

        # Actions
        hide_btn.clicked.connect(self.close_menu)

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
