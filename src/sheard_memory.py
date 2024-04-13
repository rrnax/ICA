from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout

color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class SharedMemoryStorage():
    head_labels = []
    content_rows = []

    def __init__(self):
        self.create_head_labels()
        self.create_content_rows()

    def create_head_labels(self):
        header_styles = f"""
            background-color: {color_theme[3]};
            color: {color_theme[0]};
            font-size: 18px;
        """

        for i in range(102):
            self.head_labels.append(QLabel())
            self.head_labels[i].setStyleSheet(header_styles)


    def create_content_rows(self):
        coils_style1 = f'''
           QWidget{{
               background-color: {color_theme[1]};
               color: {color_theme[3]};
               font-size: 18px;
               border-bottom: 1px solid {color_theme[3]};
           }}

           QLabel {{
               border: none
           }}
       '''

        coils_style2 = f'''
           QWidget{{
               background-color: {color_theme[0]};
               color: {color_theme[3]};
               font-size: 18px;
               border-bottom: 1px solid {color_theme[3]};
           }}

           QLabel {{
               border: none
           }}
       '''
        for i in range(12):
            row = []
            score_widget = QWidget()
            score_layout = QHBoxLayout()
            score_label = QLabel()
            score_layout.addWidget(score_label)
            score_widget.setLayout(score_layout)
            row.append(score_widget)
            score_widget.setStyleSheet(coils_style1)

            for j in range(102):

                coils_style = None
                if j % 2 == 0:
                    coils_style = coils_style1
                else:
                    coils_style = coils_style2

                move_widget = QWidget()
                move_layout = QHBoxLayout()
                move_label = QLabel()
                image_label = QLabel()
                move_layout.addWidget(image_label)
                move_layout.addWidget(move_label)
                move_widget.setLayout(move_layout)
                move_widget.setStyleSheet(coils_style)
                row.append(move_widget)
            self.content_rows.append(row)
