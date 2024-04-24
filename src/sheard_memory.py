import csv
import logging
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt


class SharedMemoryStorage:
    _instance = None
    logger = None
    head_labels = []
    content_rows = []
    color_theme = []
    history_rows = []
    openings = []
    openings_widgets = []
    endings = []
    ending_widgets = []
    color_theme_dark = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF", "#96b3e0", "#bd755c"]
    color_theme_light = ["#d4d4d4", "#FFFFFF", "#FFFFFF", "#2B2D30", "#FFFFFF", "#96b3e0", "#bd755c"]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def initialize(self):
        self.create_logger()
        self.set_dark()
        self.create_head_labels()
        self.create_content_rows()
        self.create_history_rows()
        self.load_openings()
        self.create_openings()
        self.create_endings()

    def create_logger(self):
        self.logger = logging.getLogger("InteractiveChessAssistant")
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler("../log/InteractiveChessAssistant.log")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s #### %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def create_head_labels(self):
        for i in range(102):
            self.head_labels.append(QLabel())
            self.head_labels[i].setAlignment(Qt.AlignCenter)
            self.head_labels[i].setStyleSheet(f"background-color: {self.color_theme[3]};"
                                              f"color: {self.color_theme[1]};"
                                              f"font-size: 18px;")

    def create_content_rows(self):
        for i in range(12):
            row = []
            score_label = QLabel()
            score_label.setStyleSheet(f"color: {self.color_theme[3]};"
                                      f"border: none")

            score_layout = QHBoxLayout()
            score_layout.setAlignment(Qt.AlignCenter)
            score_layout.addWidget(score_label)

            score_widget = QWidget()
            score_widget.setLayout(score_layout)
            score_widget.setStyleSheet(f"background-color: {self.color_theme[1]};"
                                       f"font-size: 18px;"
                                       f"border-bottom: 1px solid {self.color_theme[3]};")

            row.append(score_widget)

            for j in range(102):
                move_label = QLabel()
                move_label.setStyleSheet(f"color: {self.color_theme[3]};"
                                         f"border: none")

                image_label = QLabel()
                image_label.setStyleSheet(f"border: none")

                move_layout = QHBoxLayout()
                move_layout.setContentsMargins(0, 0, 0, 0)
                move_layout.setSpacing(10)
                move_layout.addWidget(image_label)
                move_layout.addWidget(move_label)
                move_layout.setAlignment(Qt.AlignCenter)

                move_widget = QWidget()
                move_widget.setLayout(move_layout)

                if j % 2 == 0:
                    move_widget.setStyleSheet(f"background-color: {self.color_theme[0]};"
                                              f"font-size: 18px;"
                                              f"border-bottom: 1px solid {self.color_theme[3]};")
                else:
                    move_widget.setStyleSheet(f"background-color: {self.color_theme[1]};"
                                              f"font-size: 18px;"
                                              f"border-bottom: 1px solid {self.color_theme[3]};")

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

    def create_openings(self):
        for opening in self.openings:
            opening_widget = QListWidgetItem(opening[0])
            self.openings_widgets.append(opening_widget)

    def create_endings(self):
        for ending in self.endings:
            ending_widget = QListWidgetItem(ending[0])
            self.ending_widgets.append(ending_widget)

    def find_opening(self, name):
        for item in self.openings:
            if item[0] == name:
                return item[1]

    def set_dark(self):
        self.color_theme = self.color_theme_dark

    def set_light(self):
        self.color_theme = self.color_theme_light

    def update_options_list(self):
        for i in range(102):
            self.head_labels[i].setStyleSheet(f"background-color: {self.color_theme[3]};"
                                              f"color: {self.color_theme[0]};"
                                              f"font-size: 18px;")

        for row in self.content_rows:
            row[0].layout().itemAt(0).widget().setStyleSheet(f"color: {self.color_theme[3]};"
                                                             f"border: none")
            row[0].setStyleSheet(f"background-color: {self.color_theme[0]};"
                                 f"font-size: 18px;"
                                 f"border-bottom: 1px solid {self.color_theme[3]};")

            for i in range(1, 102):
                row[i].layout().itemAt(1).widget().setStyleSheet(f"color: {self.color_theme[3]};"
                                                                 f"border: none")
                if i % 2 == 0:
                    row[i].setStyleSheet(f"background-color: {self.color_theme[1]};"
                                         f"font-size: 18px;"
                                         f"border-bottom: 1px solid {self.color_theme[3]};")
                else:
                    row[i].setStyleSheet(f"background-color: {self.color_theme[0]};"
                                         f"font-size: 18px;"
                                         f"border-bottom: 1px solid {self.color_theme[3]};")

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

    def load_openings(self):
        openings_csv = "../resources/schemas/debiuts.csv"
        with open(openings_csv, 'r', encoding="utf-8") as openings_file:
            csv_reader = csv.reader(openings_file, delimiter=";")
            for row in csv_reader:
                self.openings.append(row)
