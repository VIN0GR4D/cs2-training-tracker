from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout
from peewee import SqliteDatabase, Model, DateField, BooleanField, IntegerField, FloatField, TextField

db = SqliteDatabase('trainings.db')

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

class StatisticsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.general_stats_group = QGroupBox("Общая статистика")
        self.general_stats_layout = QFormLayout()
        self.general_stats_group.setLayout(self.general_stats_layout)
        layout.addWidget(self.general_stats_group)

        self.official_stats_group = QGroupBox("Официальные игры")
        self.official_stats_layout = QFormLayout()
        self.official_stats_group.setLayout(self.official_stats_layout)
        layout.addWidget(self.official_stats_group)

        self.unofficial_stats_group = QGroupBox("Обычные игры")
        self.unofficial_stats_layout = QFormLayout()
        self.unofficial_stats_group.setLayout(self.unofficial_stats_layout)
        layout.addWidget(self.unofficial_stats_group)

        self.last_match_group = QGroupBox("Предыдущая игра")
        self.last_match_layout = QFormLayout()
        self.last_match_group.setLayout(self.last_match_layout)
        layout.addWidget(self.last_match_group)

        self.update_statistics()

    def update_statistics(self):
        # Общая статистика
        total_kills, total_deaths, kd_ratio, rating = self.calculate_stats()
        self.general_stats_layout.addRow("Total Kills:", QLabel(str(total_kills)))
        self.general_stats_layout.addRow("Total Deaths:", QLabel(str(total_deaths)))
        self.general_stats_layout.addRow("K/D Ratio:", QLabel(f"{kd_ratio:.2f}"))
        self.general_stats_layout.addRow("Rating 2.0:", QLabel(f"{rating:.2f}"))

        # Статистика официальных игр
        total_kills, total_deaths, kd_ratio, rating = self.calculate_stats(official=True)
        self.official_stats_layout.addRow("Total Kills:", QLabel(str(total_kills)))
        self.official_stats_layout.addRow("Total Deaths:", QLabel(str(total_deaths)))
        self.official_stats_layout.addRow("K/D Ratio:", QLabel(f"{kd_ratio:.2f}"))
        self.official_stats_layout.addRow("Rating 2.0:", QLabel(f"{rating:.2f}"))

        # Статистика обычных игр
        total_kills, total_deaths, kd_ratio, rating = self.calculate_stats(official=False)
        self.unofficial_stats_layout.addRow("Total Kills:", QLabel(str(total_kills)))
        self.unofficial_stats_layout.addRow("Total Deaths:", QLabel(str(total_deaths)))
        self.unofficial_stats_layout.addRow("K/D Ratio:", QLabel(f"{kd_ratio:.2f}"))
        self.unofficial_stats_layout.addRow("Rating 2.0:", QLabel(f"{rating:.2f}"))

        # Статистика предыдущей игры
        last_match = self.get_last_match()
        if last_match:
            self.last_match_layout.addRow("Дата:", QLabel(str(last_match.date)))
            self.last_match_layout.addRow("Официальный:", QLabel("Да" if last_match.official else "Нет"))
            self.last_match_layout.addRow("Kills:", QLabel(str(last_match.kills)))
            self.last_match_layout.addRow("Assists:", QLabel(str(last_match.assists)))
            self.last_match_layout.addRow("Deaths:", QLabel(str(last_match.deaths)))
            self.last_match_layout.addRow("K/D Ratio:", QLabel(f"{last_match.kd_ratio:.2f}"))
            self.last_match_layout.addRow("Rating 2.0:", QLabel(f"{last_match.rating:.2f}"))
            self.last_match_layout.addRow("Заметки:", QLabel(last_match.notes))
        else:
            self.last_match_layout.addRow("Сообщение:", QLabel("Нет доступных данных"))

    def calculate_stats(self, official=None):
        query = Match.select()
        if official is not None:
            query = query.where(Match.official == official)

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
