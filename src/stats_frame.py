from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView
color_theme = ["#1E1F22", "#2B2D30", "#4E9F3D", "#FFC66C", "#FFFFFF"]


class StatsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        operation_layout = QHBoxLayout()
        operation_layout.setAlignment(Qt.AlignCenter)
        operation_layout.setContentsMargins(0, 0, 0, 0)

        operation_widget = QWidget(self)
        operation_widget.setObjectName("operation-layout")
        operation_widget.setFixedSize(450, 50)
        operation_widget.setLayout(operation_layout)

        history_label = QLabel("Historia", self)
        history_label.setAlignment(Qt.AlignCenter)
        history_label.setFixedSize(450, 40)
        history_label.setObjectName("history-label")

        history_widget = QWidget(self)
        history_widget.setFixedSize(450, 250)
        history_widget.setObjectName("history-widget")

        advantage_chart = QChart()

        chart_view = QChartView(advantage_chart, self)
        chart_view.setFixedSize(450, 200)
        chart_view.setObjectName("chart-view")

        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setAlignment(Qt.AlignTop)
        stats_layout.addWidget(operation_widget)
        stats_layout.addWidget(history_label)
        stats_layout.addWidget(history_widget)
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
                border-bottom: 1px solid {color_theme[3]};
            }}
            
            #history-widget {{
                border-bottom: 1px solid {color_theme[3]};
            }}
            
            #chart-view {{
                border-bottom: 1px solid {color_theme[3]};
            }}
        """)

    def update_size(self, new_size):
        self.setGeometry((new_size.width() - 1200) + 750, 0, 450, (new_size.height() - 820) + 550)
