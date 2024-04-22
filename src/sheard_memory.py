from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt


class SharedMemoryStorage:
    _instance = None
    head_labels = []
    content_rows = []
    color_theme = []
    history_rows = []
    color_theme_dark = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF", "#96b3e0", "#bd755c"]
    color_theme_light = ["#d4d4d4", "#FFFFFF", "#FFFFFF", "#2B2D30", "#FFFFFF", "#96b3e0", "#bd755c"]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def initialize(self):
        self.set_dark()
        self.create_head_labels()
        self.create_content_rows()
        self.create_history_rows()

    def create_head_labels(self):
        for i in range(102):
            self.head_labels.append(QLabel())
            self.head_labels[i].setObjectName("head-label")

    def create_content_rows(self):
        coils_style1 = "coli-label-one"
        coils_style2 = "coli-label-two"
        nonlabel = "no-border-label"

        for i in range(12):
            row = []
            score_widget = QWidget()
            score_layout = QHBoxLayout()
            score_label = QLabel()
            score_label.setObjectName(nonlabel)
            score_layout.addWidget(score_label)
            score_widget.setLayout(score_layout)
            row.append(score_widget)
            score_widget.setObjectName(coils_style1)

            for j in range(102):

                coils_style = None
                if j % 2 == 0:
                    coils_style = coils_style1
                else:
                    coils_style = coils_style2

                move_widget = QWidget()
                move_layout = QHBoxLayout()
                move_label = QLabel()
                move_label.setObjectName(nonlabel)
                image_label = QLabel()
                image_label.setObjectName(nonlabel)
                move_layout.addWidget(image_label)
                move_layout.addWidget(move_label)
                move_widget.setLayout(move_layout)
                move_widget.setObjectName(coils_style)
                row.append(move_widget)
            self.content_rows.append(row)

    def create_history_rows(self):
        label_style = "row-labels"
        back_lighter = "row-light"
        back_darker = "row-dark"
        white_style = "white-label"
        other_style = "other-label"

        for i in range(0, 150):
            no_label = QLabel()
            piece_label = QLabel()
            move_label = QLabel()
            info_label = QLabel()
            widget_row = QWidget()
            layout_row = QHBoxLayout()

            no_label.setFixedSize(50, 40)
            piece_label.setFixedSize(40, 40)
            move_label.setFixedSize(60, 40)
            info_label.setFixedSize(120, 40)
            info_label.setAlignment(Qt.AlignCenter)
            widget_row.setFixedSize(450, 40)
            layout_row.setSpacing(40)
            layout_row.setContentsMargins(15, 0, 0, 0)
            layout_row.setAlignment(Qt.AlignLeft)

            layout_row.addWidget(no_label)
            layout_row.addWidget(piece_label)
            layout_row.addWidget(move_label)
            layout_row.addWidget(info_label)
            widget_row.setLayout(layout_row)

            no_label.setStyleSheet(f"color:{self.color_theme[3]}; font-size: 18px;")
            info_label.setStyleSheet(f"color:{self.color_theme[3]}; font-size: 18px;")

            if i % 2 == 0:
                move_label.setStyleSheet(f"color:{self.color_theme[3]}; font-size: 15px;")
                widget_row.setStyleSheet(f"background-color: {self.color_theme[0]};")
            else:
                move_label.setStyleSheet(f"color: white; font-size: 15px;")
                widget_row.setStyleSheet(f"background-color: {self.color_theme[1]};")

            self.history_rows.append(widget_row)

    def set_dark(self):
        self.color_theme = self.color_theme_dark

    def set_light(self):
        self.color_theme = self.color_theme_light

    def update_history_style(self):
        for index, item in enumerate(self.history_rows):
            item.layout().itemAt(0).widget().setStyleSheet(f"color:{self.color_theme[3]}; font-size: 18px;")
            item.layout().itemAt(3).widget().setStyleSheet(f"color:{self.color_theme[3]}; font-size: 18px;")
            if index % 2 == 0:
                item.layout().itemAt(2).widget().setStyleSheet(f"color:{self.color_theme[3]}; font-size: 15px;")
                item.setStyleSheet(f"background-color: {self.color_theme[0]};")
            else:
                if self.color_theme[0] == "#1E1F22":
                    item.layout().itemAt(2).widget().setStyleSheet(f"color: white; font-size: 15px;")
                else:
                    item.layout().itemAt(2).widget().setStyleSheet(f"color: #1c51a6; font-size: 15px;")
                item.setStyleSheet(f"background-color: {self.color_theme[1]};")
