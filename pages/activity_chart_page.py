from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

class ActivityChartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.period_selector = QComboBox(self)
        self.period_selector.addItems(["Неделя", "Месяц", "90 дней"])
        self.period_selector.currentIndexChanged.connect(self.update_chart)
        layout.addWidget(self.period_selector)

        self.chart = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.chart)

        self.ax = self.chart.figure.add_subplot(111)
        self.update_chart()

    def update_chart(self):
        period = self.period_selector.currentText()
        self.ax.clear()

        if period == "Неделя":
            days = 7
        elif period == "Месяц":
            days = 30
        else:
            days = 90

        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(days)]
        dates.reverse()

        # Dummy data for the example
        trainings = [i % 3 for i in range(days)]
        matches = [i % 2 for i in range(days)]

        self.ax.plot(dates, trainings, label="Тренировки")
        self.ax.plot(dates, matches, label="Матчи")
        self.ax.legend()
        self.ax.set_title("Активность за период")
        self.ax.set_xlabel("Дата")
        self.ax.set_ylabel("Количество")

        self.chart.draw()
