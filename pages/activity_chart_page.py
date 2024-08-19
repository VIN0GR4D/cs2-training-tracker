# pages/activity_chart_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QGroupBox, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
from peewee import SqliteDatabase, Model, DateField, BooleanField, CharField, TextField, IntegerField, FloatField

db = SqliteDatabase('trainings.db')

class Training(Model):
    date = DateField()
    map = CharField()
    goal = CharField()
    description = TextField()

    class Meta:
        database = db

class Match(Model):
    date = DateField()
    official = BooleanField()
    kills = IntegerField()
    assists = IntegerField()
    deaths = IntegerField()
    kd_ratio = FloatField()
    rating = FloatField()
    notes = TextField()

    class Meta:
        database = db

class ActivityChartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.period_selector = QComboBox(self)
        self.period_selector.addItems(["Неделя", "Месяц", "90 дней"])
        self.period_selector.currentIndexChanged.connect(self.update_chart)
        layout.addWidget(self.period_selector)

        main_layout = QHBoxLayout()
        layout.addLayout(main_layout)

        self.chart = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(self.chart)

        self.ax = self.chart.figure.add_subplot(111)

        # Группировка статистики и графиков
        stats_layout = QVBoxLayout()
        main_layout.addLayout(stats_layout)

        self.general_stats_group = QGroupBox("Общая статистика")
        self.general_stats_layout = QGridLayout()
        self.general_stats_group.setLayout(self.general_stats_layout)
        stats_layout.addWidget(self.general_stats_group)

        self.last_match_group = QGroupBox("Последний матч")
        self.last_match_layout = QVBoxLayout()
        self.last_match_group.setLayout(self.last_match_layout)
        stats_layout.addWidget(self.last_match_group)

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

        training_counts = self.get_counts(Training, dates)
        match_counts = self.get_counts(Match, dates)

        self.ax.plot(dates, training_counts, label="Тренировки")
        self.ax.plot(dates, match_counts, label="Матчи")
        self.ax.legend()
        self.ax.set_title("Активность за период")
        self.ax.set_xlabel("Дата")
        self.ax.set_ylabel("Количество")

        self.chart.draw()

        # Обновляем статистику
        self.update_statistics()

    def get_counts(self, model, dates):
        counts = []
        for date in dates:
            count = model.select().where(model.date == date).count()
            counts.append(count)
        return counts

    def update_statistics(self):
        # Общая статистика
        total_kills, total_deaths, kd_ratio, rating = self.calculate_stats()
        self.general_stats_layout.addWidget(QLabel("Total Kills:"), 0, 0)
        self.general_stats_layout.addWidget(QLabel(str(total_kills)), 0, 1)
        self.general_stats_layout.addWidget(QLabel("Total Deaths:"), 1, 0)
        self.general_stats_layout.addWidget(QLabel(str(total_deaths)), 1, 1)
        self.general_stats_layout.addWidget(QLabel("K/D Ratio:"), 2, 0)
        self.general_stats_layout.addWidget(QLabel(f"{kd_ratio:.2f}"), 2, 1)
        self.general_stats_layout.addWidget(QLabel("Rating 2.0:"), 3, 0)
        self.general_stats_layout.addWidget(QLabel(f"{rating:.2f}"), 3, 1)

        # Последний матч
        last_match = self.get_last_match()
        if last_match:
            self.last_match_layout.addWidget(QLabel(f"Дата: {last_match.date}"))
            self.last_match_layout.addWidget(QLabel(f"Официальный: {'Да' if last_match.official else 'Нет'}"))
            self.last_match_layout.addWidget(QLabel(f"Kills: {last_match.kills}"))
            self.last_match_layout.addWidget(QLabel(f"Assists: {last_match.assists}"))
            self.last_match_layout.addWidget(QLabel(f"Deaths: {last_match.deaths}"))
            self.last_match_layout.addWidget(QLabel(f"K/D Ratio: {last_match.kd_ratio:.2f}"))
            self.last_match_layout.addWidget(QLabel(f"Rating 2.0: {last_match.rating:.2f}"))
        else:
            self.last_match_layout.addWidget(QLabel("Нет данных о последнем матче"))

    def calculate_stats(self):
        query = Match.select()

        total_kills = sum(match.kills for match in query)
        total_deaths = sum(match.deaths for match in query)
        kd_ratio = total_kills / total_deaths if total_deaths > 0 else 0
        rating = sum(match.rating for match in query) / len(query) if len(query) > 0 else 0

        return total_kills, total_deaths, kd_ratio, rating

    def get_last_match(self):
        try:
            return Match.select().order_by(Match.date.desc()).get()
        except Match.DoesNotExist:
            return None
