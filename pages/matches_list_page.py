from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QSizePolicy, QPushButton, QMessageBox, QMenu, QToolButton
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

class MatchesListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(QLabel("Список матчей:"))
        self.layout.addWidget(self.scroll_area)

        self.update_list()

    def update_list(self):
        # Очистка текущего списка
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        # Получение списка матчей из базы данных
        matches = Match.select()
        for match in matches:
            match_frame = QFrame()
            match_frame.setFrameShape(QFrame.Box)
            match_frame.setFrameShadow(QFrame.Raised)
            match_layout = QVBoxLayout()

            date_label = QLabel(f"Дата: {match.date}")
            official_label = QLabel(f"Официальный: {'Да' if match.official else 'Нет'}")
            kills_label = QLabel(f"Kills: {match.kills}")
            assists_label = QLabel(f"Assists: {match.assists}")
            deaths_label = QLabel(f"Deaths: {match.deaths}")
            kd_ratio_label = QLabel(f"K/D Ratio: {match.kd_ratio:.2f}")
            rating_label = QLabel(f"Rating 2.0: {match.rating:.2f}")
            notes_label = QLabel(f"Заметки: {match.notes}")

            # Создание кнопки с выпадающим меню
            action_button = QToolButton()
            action_button.setText("Действия")
            action_button.setPopupMode(QToolButton.InstantPopup)
            menu = QMenu(action_button)
            delete_action = menu.addAction("Удалить")
            delete_action.triggered.connect(lambda _, m=match: self.delete_match(m))
            action_button.setMenu(menu)

            match_layout.addWidget(date_label)
            match_layout.addWidget(official_label)
            match_layout.addWidget(kills_label)
            match_layout.addWidget(assists_label)
            match_layout.addWidget(deaths_label)
            match_layout.addWidget(kd_ratio_label)
            match_layout.addWidget(rating_label)
            match_layout.addWidget(notes_label)
            match_layout.addWidget(action_button)

            match_frame.setLayout(match_layout)
            match_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            match_frame.setStyleSheet("QFrame { margin: 5px; padding: 5px; } QLabel { margin: 1px; }")

            self.scroll_layout.addWidget(match_frame)

    def delete_match(self, match):
        confirm = QMessageBox.question(self, "Подтверждение удаления", "Вы уверены, что хотите удалить этот матч?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            match.delete_instance()
            self.update_list()
