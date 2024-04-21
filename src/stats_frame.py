from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from sheard_memory import SharedMemoryStorage


class StatsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic_board = self.parent().logic_board
        self.storage = SharedMemoryStorage()
        self.graphic_board = None
        self.mode_label = None

        # Items
        self.again_btn = QPushButton()
        self.move_back_btn = QPushButton()
        self.move_froward_btn = QPushButton()
        self.surrender_btn = QPushButton()
        self.draw_btn = QPushButton()
        self.board_rotation = QPushButton()
        self.history_area = QScrollArea()
        self.space_item = QWidget()
        self.operation_widget = QWidget(self)
        self.history_label = QLabel("Historia ruchów")
        self.history_widget = QWidget()
        self.empty_label = QLabel("Pusto")
        self.game_label = QLabel("Tryb: Gra")
        self.analyze_label = QLabel("Tryb: Analiza")

        # Layouts
        self.operation_layout = QHBoxLayout()
        self.layout_history = QVBoxLayout()

        # Create container
        self.set_items_properties()
        self.sets_layouts()
        self.set_general_properties()
        self.assign_actions()
        self.stats_style = self.create_style()
        self.setStyleSheet(self.stats_style)
        self.set_game_label()
        self.hide_history_rows()
        self.empty_history()
        self.update_buttons()

    # Connect button about game to actions
    def assign_actions(self):
        self.board_rotation.clicked.connect(self.parentWidget().game_frame.game_scene.rotate_board)
        self.again_btn.clicked.connect(self.logic_board.restart)
        self.move_back_btn.clicked.connect(self.logic_board.valid_undo)
        self.move_froward_btn.clicked.connect(self.logic_board.valid_forward)
        self.surrender_btn.clicked.connect(self.surrender)

    def set_general_properties(self):
        self.setGeometry(750, 0, 450, 550)
        self.setObjectName("stats-frame")

    def sets_layouts(self):
        # Layout with buttons
        self.operation_layout.setAlignment(Qt.AlignCenter)
        self.operation_layout.setContentsMargins(0, 0, 0, 0)
        self.operation_layout.addWidget(self.again_btn)
        self.operation_layout.addWidget(self.move_back_btn)
        self.operation_layout.addWidget(self.move_froward_btn)
        self.operation_layout.addWidget(self.surrender_btn)
        self.operation_layout.addWidget(self.draw_btn)
        self.operation_layout.addWidget(self.board_rotation)
        self.operation_layout.addWidget(self.space_item)
        self.operation_layout.addWidget(self.game_label)
        self.operation_layout.addWidget(self.analyze_label)
        self.operation_widget.setLayout(self.operation_layout)

        # History layout
        self.layout_history.setContentsMargins(0, 0, 0, 0)
        self.layout_history.setSpacing(0)
        self.layout_history.setAlignment(Qt.AlignCenter)
        self.layout_history.addWidget(self.empty_label)
        for item in self.storage.history_rows:
            self.layout_history.addWidget(item)
        self.history_widget.setLayout(self.layout_history)

        # General layout
        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(0)
        stats_layout.setAlignment(Qt.AlignTop)
        stats_layout.addWidget(self.operation_widget)
        stats_layout.addWidget(self.history_label)
        stats_layout.addWidget(self.history_area)
        self.setLayout(stats_layout)

    def set_items_properties(self):
        # From start button
        self.again_btn.setFixedSize(40, 40)
        self.again_btn.setIconSize(QSize(40, 40))
        self.again_btn.setToolTip("Od nowa")
        self.again_btn.setIcon((QIcon("../resources/again.png")))
        self.again_btn.setCursor((QCursor(Qt.PointingHandCursor)))
        self.again_btn.setObjectName("again-btn")

        # Move back
        self.move_back_btn.setFixedSize(40, 40)
        self.move_back_btn.setIconSize(QSize(30, 30))
        self.move_back_btn.setToolTip("Ruch wstecz")
        self.move_back_btn.setIcon(QIcon("../resources/back_arrow_smaller.png"))
        self.move_back_btn.setCursor((QCursor(Qt.PointingHandCursor)))
        self.move_back_btn.setObjectName("move-back-btn")

        # Move forward
        self.move_froward_btn.setFixedSize(40, 40)
        self.move_froward_btn.setIconSize(QSize(30, 30))
        self.move_froward_btn.setToolTip("Ruch naprzód")
        self.move_froward_btn.setIcon(QIcon("../resources/forward_arrow.png"))
        self.move_froward_btn.setCursor((QCursor(Qt.PointingHandCursor)))
        self.move_froward_btn.setObjectName("move-forward")

        # Surrender button
        self.surrender_btn.setFixedSize(40, 40)
        self.surrender_btn.setIconSize(QSize(30, 30))
        self.surrender_btn.setToolTip("Poddaj")
        self.surrender_btn.setIcon(QIcon("../resources/surrender.png"))
        self.surrender_btn.setCursor((QCursor(Qt.PointingHandCursor)))
        self.surrender_btn.setObjectName("surrender-btn")

        # Draw button
        self.draw_btn.setFixedSize(40, 40)
        self.draw_btn.setIconSize(QSize(30, 30))
        self.draw_btn.setToolTip("Zaproponuj remis")
        self.draw_btn.setIcon(QIcon("../resources/draw.png"))
        self.draw_btn.setCursor((QCursor(Qt.PointingHandCursor)))
        self.draw_btn.setObjectName("draw-btn")

        # Spacing between game type and buttons
        self.space_item.setFixedSize(20, 40)

        # Rotate board
        self.board_rotation.setFixedSize(40, 40)
        self.board_rotation.setIcon(QIcon("../resources/rotation.png"))
        self.board_rotation.setCursor(QCursor(Qt.PointingHandCursor))
        self.board_rotation.setIconSize(QSize(30, 30))
        self.board_rotation.setToolTip("Obróć plansze")
        self.board_rotation.setObjectName("rotate-btn")

        # Scroll Area
        self.history_area.setFixedSize(450, 250)
        self.history_area.setContentsMargins(0, 0, 0, 0)
        self.history_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_area.setWidget(self.history_widget)
        self.history_area.setObjectName("scroll-history")

        # Buttons widget
        self.operation_widget.setObjectName("operation-layout")
        self.operation_widget.setFixedSize(450, 50)

        # Label for history
        self.history_label.setAlignment(Qt.AlignCenter)
        self.history_label.setFixedSize(450, 40)
        self.history_label.setObjectName("history-label")

        # Widget for history
        self.history_widget.setObjectName("history-widget")

        # Empty label
        self.empty_label.setFixedSize(450, 40)
        self.empty_label.setObjectName("empty")
        self.empty_label.setAlignment(Qt.AlignCenter)

        # Mode labels
        self.analyze_label.setStyleSheet(f"padding: 5px; color: white; background-color: #144d91; font-size: 18px; "
                                         f"border: 1px solid #144d91; border-radius: 10px;")
        self.game_label.setStyleSheet(f"padding: 5px; color: white; background-color: #20a16d; font-size: 18px; "
                                      f"border: 1px solid #20a16d; border-radius: 10px;")

    # On window resize
    def update_size(self, new_size):
        self.setGeometry((new_size.width() - 1200) + 750, 0, 450, (new_size.height() - 820) + 550)
        self.history_area.setFixedSize(450, (new_size.height() - 820) + 250)

    # Set type label
    def set_game_label(self):
        if self.logic_board.mode == "analyze":
            self.game_label.hide()
            self.analyze_label.show()
        elif self.logic_board.mode == "game":
            self.analyze_label.hide()
            self.game_label.show()

    # History containers update
    def update_history(self):
        if self.logic_board.advanced_history:
            self.hide_history_rows()
            self.empty_label.hide()
            row_amount = len(self.logic_board.advanced_history)
            self.history_widget.resize(QSize(450, row_amount * 40))
            for index, element in enumerate(reversed(self.logic_board.advanced_history)):
                move = element.get("move")
                move_str = move.uci()
                piece = element.get("piece")
                add_info = element.get("about")
                self.storage.history_rows[index].layout().itemAt(0).widget().setText(str(row_amount - index) + ".")
                pixmap = piece.image
                pixmap = pixmap.scaled(QSize(25, 25), transformMode=Qt.SmoothTransformation)
                self.storage.history_rows[index].layout().itemAt(1).widget().setPixmap(pixmap)
                self.storage.history_rows[index].layout().itemAt(2).widget().setText(move_str[:2] +
                                                                                     " -> " + move_str[2:])
                self.storage.history_rows[index].layout().itemAt(3).widget().setText(add_info)
                self.storage.history_rows[index].show()
        else:
            self.empty_history()

    # Show special container if history is empty
    def empty_history(self):
        self.hide_history_rows()
        self.history_widget.resize(QSize(450, 40))
        self.empty_label.show()

    # Change button in actions
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

    def update_theme(self):
        style = self.create_style()
        self.setStyleSheet(style)
        self.storage.update_history_style()

    # Clear history containers
    def hide_history_rows(self):
        for item in self.storage.history_rows:
            item.hide()

    def create_style(self):
        return f"""
            #stats-frame {{
                background-color: {self.storage.color_theme[0]};
            }}
            
            #operation-layout {{
                background-color: {self.storage.color_theme[1]};
                border-bottom: 1px solid {self.storage.color_theme[3]};
                border-left: 1px solid {self.storage.color_theme[3]};
                border-top: none;
            }}
            
            #history-label {{
                background-color: {self.storage.color_theme[1]};
                color: {self.storage.color_theme[3]};
                font-size: 20px;
                border-left: 1px solid {self.storage.color_theme[3]};
                border-top: none;
            }}
            
            #history-widget {{
                background-color: {self.storage.color_theme[1]};
            }}
            
            #row-labels {{ 
                color:{self.storage.color_theme[3]}; 
                font-size: 18;
            }}
            
            #row-dark {{
                background-color: {self.storage.color_theme[0]};
            }}
            
            #row-light {{
                background-color: {self.storage.color_theme[1]};
            }}
            
            #white-label {{
                color: white; 
                font-size: 18;
            }}
                            
            #scroll-history {{
                background-color: {self.storage.color_theme[0]};
                border-top: none;
                border-left: 1px solid {self.storage.color_theme[3]};
                border-bottom: 1px solid {self.storage.color_theme[3]};
            }}
            
            #empty {{
                background-color:{self.storage.color_theme[0]};
                color:{self.storage.color_theme[3]}; 
                font-size: 18;
            }}
            
            #again-btn, #move-back-btn, #move-forward, #surrender-btn, #draw-btn, #rotate-btn {{
                background-color: {self.storage.color_theme[1]};
                border: 1px solid {self.storage.color_theme[1]};
            }}
            
            #again-btn:hover, #move-back-btn:hover, #move-forward:hover, #surrender-btn:hover, #draw-btn:hover, 
            #rotate-btn:hover {{ background-color: {self.storage.color_theme[3]};
                border-radius: 10px;
            }}
        """

# <a href="https://www.flaticon.com/free-icons/back-arrow" title="back arrow icons">Back arrow icons created by Vector Squad - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/sports-and-competition" title="sports and competition icons">Sports and competition icons created by BZZRINCANTATION - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/reset" title="reset icons">Reset icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/white-flag" title="white flag icons">White flag icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/back" title="back icons">Back icons created by Google - Flaticon</a>
