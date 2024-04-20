from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout


class SharedMemoryStorage:
    _instance = None
    head_labels = []
    content_rows = []
    color_theme = []
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

    def set_dark(self):
        self.color_theme = self.color_theme_dark

    def set_light(self):
        self.color_theme = self.color_theme_light

