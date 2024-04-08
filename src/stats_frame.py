from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt, QSize, QPointF
from PyQt5.QtGui import QIcon, QCursor, QPixmap, QColor, QPainter, QPen
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from logic_board import LogicBoard
color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF", "#20a16d"]

# <a href="https://www.flaticon.com/free-icons/back-arrow" title="back arrow icons">Back arrow icons created by Vector Squad - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/sports-and-competition" title="sports and competition icons">Sports and competition icons created by BZZRINCANTATION - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/reset" title="reset icons">Reset icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/white-flag" title="white flag icons">White flag icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/back" title="back icons">Back icons created by Google - Flaticon</a>
moves = ["e2e4", "e7e6", "f1c4", "g8f6", "g1f3", "f6e4", "e1g1"]


class StatsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic_board = LogicBoard()
        self.graphic_board = self.parent().game_frame.game_scene
        self.logic_board.stats_frame = self
        self.history_items = []
        self.mode_label = None

        again_btn = QPushButton()
        again_btn.setFixedSize(40, 40)
        again_btn.setIcon((QIcon("../resources/again.png")))
        again_btn.setCursor((QCursor(Qt.PointingHandCursor)))
        again_btn.setIconSize(QSize(40, 40))

        move_back_btn = QPushButton()
        move_back_btn.setFixedSize(40, 40)
        move_back_btn.setIcon(QIcon("../resources/back_arrow_smaller.png"))
        move_back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        move_back_btn.setIconSize(QSize(30, 30))

        move_froward_btn = QPushButton()
        move_froward_btn.setFixedSize(40, 40)
        move_froward_btn.setIcon(QIcon("../resources/forward_arrow.png"))
        move_froward_btn.setCursor(QCursor(Qt.PointingHandCursor))
        move_froward_btn.setIconSize(QSize(30, 30))

        surrender_btn = QPushButton()
        surrender_btn.setFixedSize(40, 40)
        surrender_btn.setIcon(QIcon("../resources/surrender.png"))
        surrender_btn.setCursor(QCursor(Qt.PointingHandCursor))
        surrender_btn.setIconSize(QSize(30, 30))

        draw_btn = QPushButton()
        draw_btn.setFixedSize(40, 40)
        draw_btn.setIcon(QIcon("../resources/draw.png"))
        draw_btn.setCursor(QCursor(Qt.PointingHandCursor))
        draw_btn.setIconSize(QSize(30, 30))

        board_rotation = QPushButton()
        board_rotation.setFixedSize(40, 40)
        board_rotation.setIcon(QIcon("../resources/loader.png"))
        board_rotation.setCursor(QCursor(Qt.PointingHandCursor))
        board_rotation.setIconSize(QSize(30, 30))

        space_item = QWidget()
        space_item.setFixedSize(20, 40)

        self.operation_layout = QHBoxLayout()
        self.operation_layout.setAlignment(Qt.AlignCenter)
        self.operation_layout.setContentsMargins(0, 0, 0, 0)
        self.operation_layout.addWidget(again_btn)
        self.operation_layout.addWidget(move_back_btn)
        self.operation_layout.addWidget(move_froward_btn)
        self.operation_layout.addWidget(surrender_btn)
        self.operation_layout.addWidget(draw_btn)
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

        self.advantage_chart = QChart()
        self.advantage_chart.legend().hide()
        self.advantage_chart.setContentsMargins(0, 0, 0, 0)
        self.advantage_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.advantage_chart.setTitleBrush(QColor(color_theme[3]))
        self.advantage_chart.setBackgroundBrush(QColor(color_theme[0]))
        self.update_chart()

        chart_view = QChartView(self.advantage_chart, self)
        # chart_view.setFixedSize(450, 210)
        chart_view.setContentsMargins(0, 0, 0, 0)
        chart_view.setBackgroundBrush(QColor(color_theme[0]))
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setObjectName("chart-view")

        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(0)
        stats_layout.setAlignment(Qt.AlignTop)
        stats_layout.addWidget(operation_widget)
        stats_layout.addWidget(history_label)
        stats_layout.addWidget(self.history_area)
        stats_layout.addWidget(chart_view)

        # Set frame general options
        self.setGeometry(750, 0, 450, 550)
        self.setObjectName("stats-frame")
        self.setLayout(stats_layout)
        self.setStyleSheet(f"""
            #stats-frame {{
                background-color: {color_theme[1]};
                border-left: 1px solid {color_theme[3]};
            }}
            
            #operation-layout {{
                border-bottom: 1px solid {color_theme[3]};
            }}
            
            #history-label {{
                color: {color_theme[3]};
                font-size: 20px;
            }}
            
            #history-widget {{
                background-color: {color_theme[1]};
            }}
            
            #chart-view {{
                border-top: 1px solid {color_theme[3]};
            }}
            
            
            QPushButton {{
                background-color: {color_theme[1]};
                border: 1px solid {color_theme[1]};
            }}
            
            QPushButton:hover {{
                background-color: {color_theme[3]};
                border-radius: 10px;
            }}
            
            QScrollArea {{
                background-color: {color_theme[0]};
                border-top: none;
                border-left: 1px solid {color_theme[3]};
            }}
            
            QScrollBar:vertical {{
                background-color: {color_theme[1]};
                color: {color_theme[3]};
                border: 1px solid {color_theme[3]}
            }}
            
            QScrollBar::handle:vertical {{
                border: none;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: {color_theme[3]};
                border: none;
            }}
            
            QLabel {{
                color: {color_theme[3]};
                font-size: 18 ;
            }}
            
            QChart {{
                background-color: {color_theme[1]};
            }}
        """)

        board_rotation.clicked.connect(self.parentWidget().game_frame.game_scene.rotate_board)
        again_btn.clicked.connect(self.logic_board.restart)
        move_back_btn.clicked.connect(self.remove_last_move)

        self.set_game_label("analyze")
        self.empty_history()

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
                piece_img = element.get("image")
                add_info = element.get("about")
                style = None
                if (row_amount - index - 1) % 2 == 0:
                    style = f"""
                        #move-label {{
                            color: white;
                        }}
                    """
                else:
                    style = f"""
                        #move-label {{
                            color: {color_theme[3]};
                        }}
                    """
                if index % 2 == 0:
                    style += f"""
                        QWidget {{
                            background-color: {color_theme[0]};
                        }}
                    """
                else:
                    style += f"""
                        QWidget {{
                            background-color: {color_theme[1]};
                        }}
                    """

                piece_label = QLabel()
                piece_label.setFixedSize(60, 40)
                piece_label.setPixmap(piece_img.scaled(QSize(20, 20)))

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

    def clear_history(self):
        for widget in self.history_items:
            self.layout_history.removeWidget(widget)
            widget.deleteLater()
        self.history_items.clear()
        self.history_widget.resize(QSize(0, 0))

    def empty_history(self):
        empty_label = QLabel("Pusto")
        empty_label.setFixedSize(450, 40)
        empty_label.setStyleSheet(f"background-color: {color_theme[0]};")
        empty_label.setAlignment(Qt.AlignCenter)
        self.layout_history.addWidget(empty_label)
        self.history_items.append(empty_label)
        self.history_widget.resize(QSize(450, 40))

    def remove_last_move(self):
        if self.logic_board.advanced_history:
            deleted_move = self.logic_board.pop()
            print("XD0")
            piece = self.graphic_board.find_piece(deleted_move.uci()[2:])
            print("Xd2")
            piece.graphic_move(deleted_move.uci()[:2])
            # advantage_piece = self.logic_board.advanced_history.pop()
            # if advantage_piece.get("about") == "Bicie":
            #     print(advantage_piece)
            #     self.graphic_board.return_piece(deleted_move.uci()[2:])

            if len(self.logic_board.advanced_history) == 0:
                last_field = self.graphic_board.find_field(deleted_move.uci()[:2])
                last_field.setBrush(QColor(last_field.orginal_brush))
                self.clear_history()
                self.empty_history()
            else:
                last_move = self.logic_board.advanced_history[-1].get("move")
                last_field = self.graphic_board.find_field(last_move.uci()[:2])
                self.graphic_board.clear_circles()
                self.graphic_board.clear_captures()
                self.graphic_board.highlight_field(last_field)
                self.update_history()

    def update_chart(self):
        series = QLineSeries()

        data = [
            QPointF(0, 0.0),
            QPointF(1, -0.4),
            QPointF(2, -2.0),
            QPointF(3, 1.2),
            QPointF(4, 2.0)
        ]

        pen = QPen(QColor("#20a16d"))
        pen.setWidth(3)

        axis_X = QValueAxis()
        axis_X.setTickCount(5)
        axis_X.setRange(0, 4)
        axis_X.setLabelFormat("%d")
        axis_X.setLabelsColor(QColor(color_theme[4]))
        axis_X.setTitleText("Ruch")
        axis_X.setTitleBrush(QColor(color_theme[3]))
        axis_X.setGridLineColor(QColor(color_theme[1]))

        axis_Y = QValueAxis()
        axis_Y.setTickCount(5)
        axis_Y.setRange(-2.0, 2.00)
        axis_Y.setLabelsColor(QColor(color_theme[4]))
        axis_Y.setTitleText("Przewaga")
        axis_Y.setTitleBrush(QColor(color_theme[3]))
        axis_Y.setGridLineColor(QColor(color_theme[1]))

        self.advantage_chart.addAxis(axis_X, Qt.AlignmentFlag.AlignBottom)
        self.advantage_chart.addAxis(axis_Y, Qt.AlignmentFlag.AlignLeft)

        series.append(data)
        self.advantage_chart.addSeries(series)
        series.setPen(pen)

        # self.advantage_chart.createDefaultAxes()
        # advantage_axis = QValueAxis()
        # advantage_axis.setRange(-2.0, 2.0)
        #

