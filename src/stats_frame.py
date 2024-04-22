from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QCursor
from sheard_memory import SharedMemoryStorage
from math import ceil


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
        self.turn_widget = QWidget()
        self.turn_label = QLabel("RUCH CZARNYCH")
        self.probability_widget = QWidget()
        self.probability_label = QLabel("Szanse")
        self.probability_diagram = QWidget()
        self.proc_widget = QWidget()
        self.w_proc = QLabel()
        self.b_proc = QLabel()
        self.white_chance = QLabel()
        self.draw_chance = QLabel()
        self.black_chance = QLabel()

        # Layouts
        self.operation_layout = QHBoxLayout()
        self.layout_history = QVBoxLayout()
        self.turn_layout = QHBoxLayout()
        self.probability_layout = QVBoxLayout()
        self.diagram_layout = QHBoxLayout()
        self.proc_layout = QHBoxLayout()

        # Create container
        self.set_items_properties()
        self.sets_layouts()
        self.set_general_properties()
        self.assign_actions()
        self.stats_style = self.create_style()
        self.setStyleSheet(self.stats_style)
        self.set_game_label()
        self.hide_history_rows()
        self.set_turn_label()
        self.empty_history()
        self.update_buttons()

        # Turn pulse
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.pulse_turn)
        self.timer.start(1000)

        self.draw_chance.hide()

    def set_probability(self, values):
        whites = 0
        blacks = 0
        if self.logic_board.turn:
            whites = values.wins * 0.001
            blacks = values.losses * 0.001
        else:
            blacks = values.wins * 0.001
            whites = values.losses * 0.001
        draws = values.draws * 0.001

        w_pixels = ceil(whites * 420 + (draws * 420)/2)
        b_pixels = ceil(blacks * 420 + (draws * 420)/2)
        w_proc = (whites + draws/2) * 100
        b_proc = (blacks + draws/2) * 100

        self.w_proc.setText(str(round(w_proc, 1)) + "%")
        self.b_proc.setText(str(round(b_proc, 1)) + "%")

        self.white_chance.setGeometry(0, 0, w_pixels, 30)
        self.black_chance.setGeometry(w_pixels, 0, b_pixels, 30)

    def pulse_turn(self):
        self.turn_label.setVisible(not self.turn_label.isVisible())

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

        # Turn layout
        self.turn_layout.setAlignment(Qt.AlignCenter)
        self.turn_layout.addWidget(self.turn_label)
        self.turn_widget.setLayout(self.turn_layout)

        # Probability widget
        self.diagram_layout.setContentsMargins(0, 0, 0, 0)
        self.diagram_layout.setSpacing(0)
        self.diagram_layout.setAlignment(Qt.AlignLeft)
        self.diagram_layout.addWidget(self.white_chance)
        self.diagram_layout.addWidget(self.draw_chance)
        self.diagram_layout.addWidget(self.black_chance)
        self.proc_layout.setContentsMargins(0, 0, 0, 0)
        self.proc_layout.addWidget(self.w_proc)
        self.proc_layout.addStretch(1)
        self.proc_layout.addWidget(self.b_proc)
        self.proc_widget.setLayout(self.proc_layout)
        self.probability_diagram.setLayout(self.diagram_layout)
        self.probability_layout.setAlignment(Qt.AlignCenter)
        self.probability_layout.setSpacing(10)
        self.probability_layout.addWidget(self.probability_label)
        self.probability_layout.addWidget(self.proc_widget)
        self.probability_layout.addWidget(self.probability_diagram)
        self.probability_widget.setLayout(self.probability_layout)

        # General layout
        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(0)
        stats_layout.setAlignment(Qt.AlignTop)
        stats_layout.addWidget(self.operation_widget)
        stats_layout.addWidget(self.history_label)
        stats_layout.addWidget(self.history_area)
        stats_layout.addWidget(self.turn_widget)
        stats_layout.addWidget(self.probability_widget)
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

        # Turn label
        self.turn_label.setStyleSheet(f"color: {self.storage.color_theme[3]}; border: none;")
        self.turn_widget.setFixedSize(450, 40)
        self.turn_widget.setStyleSheet(
            f"background-color: {self.storage.color_theme[0]};"
            f"font-size: 20px; border-left: 1px solid {self.storage.color_theme[3]};" 
            f"border-bottom: 1px solid {self.storage.color_theme[3]};")

        # Probability widget
        self.probability_widget.setFixedSize(450, 160)
        self.probability_label.setAlignment(Qt.AlignCenter)
        self.probability_label.setStyleSheet(f"font-size: 20px; color: {self.storage.color_theme[3]};")
        self.proc_widget.setFixedSize(420, 30)
        self.proc_widget.setStyleSheet(f"font-size: 13px; color: {self.storage.color_theme[3]};")
        self.probability_diagram.setFixedSize(420, 30)
        self.probability_diagram.setStyleSheet(f"border-radius: 10px;")
        self.white_chance.setStyleSheet(f"background-color: white;")
        self.draw_chance.setStyleSheet(f"background-color: gray;")
        self.black_chance.setStyleSheet(f"background-color: black;")

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
        self.set_turn_label()

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
        self.set_turn_label()

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
        self.turn_label.setStyleSheet(f"color: {self.storage.color_theme[3]}; border: none;")
        self.turn_widget.setStyleSheet(
            f"background-color: {self.storage.color_theme[0]};"
            f"font-size: 20px; border-left: 1px solid {self.storage.color_theme[3]};"
            f"border-bottom: 1px solid {self.storage.color_theme[3]};")
        self.probability_label.setStyleSheet(f"font-size: 20px; color: {self.storage.color_theme[3]};")
        self.proc_widget.setStyleSheet(f"font-size: 13px; color: {self.storage.color_theme[3]};")
        self.proc_widget.setStyleSheet(f"font-size: 13px; color: {self.storage.color_theme[3]};")
        self.storage.update_history_style()

    # Clear history containers
    def hide_history_rows(self):
        for item in self.storage.history_rows:
            item.hide()

    def set_turn_label(self):
        if self.logic_board.turn:
            self.turn_label.setText("RUCH BIAŁYCH")
        else:
            self.turn_label.setText("RUCH CZARNYCH")

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
