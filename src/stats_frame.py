from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from logic_board import LogicBoard
from chess import square_name
from sheard_memory import color_theme


# <a href="https://www.flaticon.com/free-icons/back-arrow" title="back arrow icons">Back arrow icons created by Vector Squad - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/sports-and-competition" title="sports and competition icons">Sports and competition icons created by BZZRINCANTATION - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/reset" title="reset icons">Reset icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/white-flag" title="white flag icons">White flag icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/back" title="back icons">Back icons created by Google - Flaticon</a>


class StatsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic_board = LogicBoard()
        self.history_items = []
        self.graphic_board = None
        self.mode_label = None
        self.main_color = color_theme

        self.again_btn = QPushButton()
        self.again_btn.setFixedSize(40, 40)
        self.again_btn.setIconSize(QSize(40, 40))
        self.again_btn.setToolTip("Od nowa")
        self.again_btn.setIcon((QIcon("../resources/again.png")))
        self.again_btn.setCursor((QCursor(Qt.PointingHandCursor)))

        self.move_back_btn = QPushButton()
        self.move_back_btn.setFixedSize(40, 40)
        self.move_back_btn.setIconSize(QSize(30, 30))
        self.move_back_btn.setToolTip("Ruch wstecz")
        self.move_back_btn.setIcon(QIcon("../resources/back_arrow_smaller.png"))
        self.move_back_btn.setCursor((QCursor(Qt.PointingHandCursor)))

        self.move_froward_btn = QPushButton()
        self.move_froward_btn.setFixedSize(40, 40)
        self.move_froward_btn.setIconSize(QSize(30, 30))
        self.move_froward_btn.setToolTip("Ruch naprzód")
        self.move_froward_btn.setIcon(QIcon("../resources/forward_arrow.png"))
        self.move_froward_btn.setCursor((QCursor(Qt.PointingHandCursor)))

        self.surrender_btn = QPushButton()
        self.surrender_btn.setFixedSize(40, 40)
        self.surrender_btn.setIconSize(QSize(30, 30))
        self.surrender_btn.setToolTip("Poddaj")
        self.surrender_btn.setIcon(QIcon("../resources/surrender.png"))
        self.surrender_btn.setCursor((QCursor(Qt.PointingHandCursor)))

        self.draw_btn = QPushButton()
        self.draw_btn.setFixedSize(40, 40)
        self.draw_btn.setIconSize(QSize(30, 30))
        self.draw_btn.setToolTip("Zaproponuj remis")
        self.draw_btn.setIcon(QIcon("../resources/draw.png"))
        self.draw_btn.setCursor((QCursor(Qt.PointingHandCursor)))

        board_rotation = QPushButton()
        board_rotation.setFixedSize(40, 40)
        board_rotation.setIcon(QIcon("../resources/rotation.png"))
        board_rotation.setCursor(QCursor(Qt.PointingHandCursor))
        board_rotation.setIconSize(QSize(30, 30))
        board_rotation.setToolTip("Obróć plansze")

        space_item = QWidget()
        space_item.setFixedSize(20, 40)

        self.operation_layout = QHBoxLayout()
        self.operation_layout.setAlignment(Qt.AlignCenter)
        self.operation_layout.setContentsMargins(0, 0, 0, 0)
        self.operation_layout.addWidget(self.again_btn)
        self.operation_layout.addWidget(self.move_back_btn)
        self.operation_layout.addWidget(self.move_froward_btn)
        self.operation_layout.addWidget(self.surrender_btn)
        self.operation_layout.addWidget(self.draw_btn)
        self.operation_layout.addWidget(board_rotation)
        self.operation_layout.addWidget(space_item)
        # self.operation_layout.addWidget(self.game_type_label)

        operation_widget = QWidget(self)
        operation_widget.setObjectName("operation-layout")
        operation_widget.setFixedSize(450, 50)
        operation_widget.setLayout(self.operation_layout)

        history_label = QLabel("Historia ruchów", self)
        history_label.setAlignment(Qt.AlignCenter)
        history_label.setFixedSize(450, 40)
        history_label.setObjectName("history-label")

        self.layout_history = QVBoxLayout()
        self.layout_history.setContentsMargins(0, 0, 0, 0)
        self.layout_history.setSpacing(0)
        self.layout_history.setAlignment(Qt.AlignCenter)
        # self.update_history()

        self.history_widget = QWidget()
        self.history_widget.setObjectName("history-widget")
        self.history_widget.setLayout(self.layout_history)

        self.history_area = QScrollArea()
        self.history_area.setFixedSize(450, 250)
        self.history_area.setContentsMargins(0, 0, 0, 0)
        self.history_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_area.setWidget(self.history_widget)

        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(0)
        stats_layout.setAlignment(Qt.AlignTop)
        stats_layout.addWidget(operation_widget)
        stats_layout.addWidget(history_label)
        stats_layout.addWidget(self.history_area)

        # Set frame general options
        self.setGeometry(750, 0, 450, 550)
        self.setObjectName("stats-frame")
        self.setLayout(stats_layout)
        self.setStyleSheet(f"""
            #stats-frame {{
                background-color: {self.main_color[0]};
            }}
            
            #operation-layout {{
                background-color: {self.main_color[1]};
                border-bottom: 1px solid {self.main_color[3]};
                border-left: 1px solid {self.main_color[3]};
                border-top: none;
            }}
            
            #history-label {{
                background-color: {self.main_color[1]};
                color: {self.main_color[3]};
                font-size: 20px;
                border-left: 1px solid {self.main_color[3]};
                border-top: none;
            }}
            
            #history-widget {{
                background-color: {self.main_color[1]};
            }}
            
            #chart-view {{
                border-top: 1px solid {self.main_color[3]};
            }}
            
            QScrollArea {{
                background-color: {self.main_color[0]};
                border-top: none;
                border-left: 1px solid {self.main_color[3]};
                border-bottom: 1px solid {self.main_color[3]};
            }}
            
            QScrollBar:vertical {{
                background-color: {self.main_color[1]};
                color: {self.main_color[3]};
                border: 1px solid {self.main_color[3]}
            }}
            
            QScrollBar::handle:vertical {{
                border: none;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: {self.main_color[3]};
                border: none;
            }}
            
            QLabel {{
                color: {self.main_color[3]};
                font-size: 18 ;
            }}
            
             QPushButton {{
                background-color: {self.main_color[1]};
                border: 1px solid {self.main_color[1]};
            }}
            
            QPushButton:hover {{
                background-color: {self.main_color[3]};
                border-radius: 10px;
            }}
            
        """)

        board_rotation.clicked.connect(self.parentWidget().game_frame.game_scene.rotate_board)
        self.again_btn.clicked.connect(self.logic_board.restart)
        self.move_back_btn.clicked.connect(self.logic_board.valid_undo)
        self.move_froward_btn.clicked.connect(self.logic_board.valid_forward)
        self.surrender_btn.clicked.connect(self.surrender)

        self.set_game_label("analyze")
        self.empty_history()
        self.update_buttons()

    # On window resize
    def update_size(self, new_size):
        self.setGeometry((new_size.width() - 1200) + 750, 0, 450, (new_size.height() - 820) + 550)
        self.history_area.setFixedSize(450, (new_size.height() - 820) + 250)

    # Set type label
    def set_game_label(self, mode):
        if self.mode_label is not None:
            self.operation_layout.removeWidget(self.mode_label)
            self.mode_label.deleteLater()

        label = QLabel()
        styles = None
        if mode == "analyze":
            label.setText("Tryb: Analiza")
            styles = f"""#game-type {{
                        padding: 5px;
                        color: white;
                        background-color: #144d91;
                        font-size: 18px;
                        border: 1px solid #144d91;
                        border-radius: 10px;
                    }}"""
        elif mode == "game":
            label.setText("Tryb: Gra")
            styles = f"""#game-type {{
                        padding: 5px;
                        color: white;
                        background-color: #20a16d;
                        font-size: 18px;
                        border: 1px solid #20a16d;
                        border-radius: 10px;
                    }}"""
        label.setObjectName("game-type")
        label.setStyleSheet(styles)
        self.operation_layout.addWidget(label)
        self.mode_label = label

    # History creation
    def update_history(self):
        if self.logic_board.advanced_history:
            self.clear_history()
            row_amount = len(self.logic_board.advanced_history)
            self.history_widget.resize(QSize(450, row_amount * 40))
            for index, element in enumerate(reversed(self.logic_board.advanced_history)):
                no_label = QLabel(str(row_amount - index) + ".")
                no_label.setFixedSize(50, 40)
                move = element.get("move")
                move_str = move.uci()
                piece = element.get("piece")
                add_info = element.get("about")
                style = None
                if (row_amount - index - 1) % 2 == 0:
                    if self.main_color[0] == "#1E1F22":
                        style = f"""
                            #move-label {{
                                color: white;
                            }}
                        """
                    else:
                        style = f"""
                           #move-label {{
                               color: {self.main_color[6]};
                           }}
                        """
                else:
                    style = f"""
                        #move-label {{
                            color: {self.main_color[3]};
                        }}
                    """
                if index % 2 == 0:
                    style += f"""
                        QWidget {{
                            background-color: {self.main_color[0]};
                        }}
                    """
                else:
                    style += f"""
                        QWidget {{
                            background-color: {self.main_color[1]};
                        }}
                    """

                piece_label = QLabel()
                piece_label.setFixedSize(40, 40)
                pixmap = piece.image
                pixmap = pixmap.scaled(QSize(25, 25), transformMode=Qt.SmoothTransformation)
                piece_label.setPixmap(pixmap)

                if move_str == "0000":
                    move_label = QLabel("")
                else:
                    move_label = QLabel(move_str[:2] + " -> " + move_str[2:])
                move_label.setObjectName("move-label")
                move_label.setFixedSize(60, 40)

                info_label = QLabel(add_info)
                info_label.setFixedSize(100, 40)
                info_label.setAlignment(Qt.AlignCenter)

                layout_row = QHBoxLayout()
                layout_row.setSpacing(50)
                layout_row.setContentsMargins(15, 0, 0, 0)
                layout_row.setAlignment(Qt.AlignLeft)
                layout_row.addWidget(no_label)
                layout_row.addWidget(piece_label)
                layout_row.addWidget(move_label)
                layout_row.addWidget(info_label)

                widget_row = QWidget()
                widget_row.setFixedSize(450, 40)
                widget_row.setStyleSheet(style)
                widget_row.setLayout(layout_row)

                self.layout_history.addWidget(widget_row)
                self.history_items.append(widget_row)

        else:
            self.empty_history()

########################################################

    def clear_history(self):
        for widget in self.history_items:
            self.layout_history.removeWidget(widget)
            widget.deleteLater()
        self.history_items.clear()
        self.history_widget.resize(QSize(0, 0))

    def empty_history(self):
        self.clear_history()
        empty_label = QLabel("Pusto")
        empty_label.setFixedSize(450, 40)
        empty_label.setStyleSheet(f"background-color: {self.main_color[0]};")
        empty_label.setAlignment(Qt.AlignCenter)
        self.layout_history.addWidget(empty_label)
        self.history_items.append(empty_label)
        self.history_widget.resize(QSize(450, 40))

    def update_buttons(self):
        if self.logic_board.advanced_history:
            self.again_btn.setEnabled(True)
            self.move_back_btn.setEnabled(True)
            self.draw_btn.setEnabled(False)

        else:
            self.again_btn.setEnabled(False)
            self.move_back_btn.setEnabled(False)
            self.draw_btn.setEnabled(False)

        if self.logic_board.forward_moves:
            self.move_froward_btn.setEnabled(True)
        else:
            self.move_froward_btn.setEnabled(False)

        if self.logic_board.ended_game is None and self.logic_board.advanced_history:
            self.surrender_btn.setEnabled(True)
        else:
            self.surrender_btn.setEnabled(False)

    def surrender(self):
        self.logic_board.make_surrender()

    def update_theme(self, themes):
        self.main_color = themes
        print(self.main_color)
        style = f"""
            #stats-frame {{
                background-color: {themes[0]};
            }}
            
            #operation-layout {{
                background-color: {themes[1]};
                border-bottom: 1px solid {themes[3]};
                border-left: 1px solid {themes[3]};
                border-top: none;
            }}
            
            #history-label {{
                background-color: {themes[1]};
                color: {themes[3]};
                font-size: 20px;
                border-left: 1px solid {themes[3]};
                border-top: none;
            }}
            
            #history-widget {{
                background-color: {themes[1]};
            }}
            
            #chart-view {{
                border-top: 1px solid {themes[3]};
            }}
            
            QScrollArea {{
                background-color: {themes[0]};
                border-top: none;
                border-left: 1px solid {themes[3]};
                border-bottom: 1px solid {themes[3]};
            }}
            
            QScrollBar:vertical {{
                background-color: {themes[1]};
                color: {themes[3]};
                border: 1px solid {themes[3]}
            }}
            
            QScrollBar::handle:vertical {{
                border: none;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: {themes[3]};
                border: none;
            }}
            
            QLabel {{
                color: {themes[3]};
                font-size: 18 ;
            }}
            
             QPushButton {{
                background-color: {themes[1]};
                border: 1px solid {themes[1]};
            }}
            
            QPushButton:hover {{
                background-color: {themes[3]};
                border-radius: 10px;
            }}
            
        """
        self.setStyleSheet(style)
        self.update_history()
