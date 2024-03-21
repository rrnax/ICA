from PyQt5.QtWidgets import QFrame

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class StatsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(750, 0, 450, 550)
        self.setObjectName("stats-frame")
        self.setStyleSheet(f"""
            #stats-frame {{
                background-color: {color_theme[1]};
                border-left: 1px solid {color_theme[3]};
            }}
        """)

    def update_size(self, new_size):
        self.setGeometry((new_size.width() - 1200) + 750, 0, 450, (new_size.height() - 820) + 550)
