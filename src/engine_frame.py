from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QToolButton, QPushButton
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


color_theme = ["#191A19", "#1E5128", "#4E9F3D", "#D8E9A8", "#FFFFFF"]


class EngineFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Nodes elements
        self.engine_label = QLabel("Engine: Stockfish")
        self.depth_label = QLabel("Depth: 20")
        self.moves_filter_button = QToolButton()
        self.moves_filter_button.setFixedSize(100, 50)
        self.moves_filter_button.setText("Filters")
        self.moves_filter_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.engine_settings_button = QPushButton("Settings")
        self.engine_settings_button.setFixedSize(100, 50)
        self.engine_settings_button.setCursor(QCursor(Qt.PointingHandCursor))

        # Layouts parts
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(20, 0, 0, 0)
        left_layout.addWidget(self.engine_label)
        left_layout.addWidget(self.depth_label)
        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.moves_filter_button)
        right_layout.addWidget(self.engine_settings_button)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # Layout
        self.engine_frame_layout = QHBoxLayout()
        self.engine_frame_layout.addWidget(left_widget)
        self.engine_frame_layout.addWidget(right_widget)
        self.engine_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.engine_frame_layout.setSpacing(400)

        # Frame
        self.setLayout(self.engine_frame_layout)
        self.setGeometry(0, 550, 1200, 70)
        self.setObjectName("engine-frame")
        self.setStyleSheet(f"""
            #engine-frame {{
                border-top: 1px solid {color_theme[3]};
                border-bottom: 1px solid {color_theme[3]};
            }}
                
            QWidget {{
                color: {color_theme[3]};
                font-size: 20px;
            }}
             
            QToolButton {{
                border: 1px solid {color_theme[3]};
                border-radius: 10px;
            }}
            
             QToolButton:hover {{
                color: black;
                background-color: {color_theme[3]};
                cursor: pointer;
            }}
            
            QPushButton {{
                border: 1px solid {color_theme[3]};
                border-radius: 10px;
            }}
            
            QPushButton:hover {{
                color: black;
                background-color: {color_theme[3]};
            }}
            """)

    def change_for_window_resize(self, new_size):
        self.engine_frame_layout.setSpacing(400 + new_size.width()-1200)
        self.setGeometry(0, (new_size.height() - 820) + 550, (new_size.width() - 1200) + 1200, 70)


