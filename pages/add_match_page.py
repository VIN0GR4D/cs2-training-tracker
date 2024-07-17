from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtCore import QDate, pyqtSignal
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

db.connect()
db.create_tables([Match], safe=True)

class AddMatchPage(QWidget):
    match_added = pyqtSignal()  # Сигнал, который испускается при добавлении матча

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.date_label = QLabel("Дата:")
        layout.addWidget(self.date_label)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        self.official_label = QLabel("Официальный матч:")
        layout.addWidget(self.official_label)
        self.official_input = QComboBox()
        self.official_input.addItems(["Да", "Нет"])
        layout.addWidget(self.official_input)

        self.kills_label = QLabel("Kills:")
        layout.addWidget(self.kills_label)
        self.kills_input = QLineEdit()
        layout.addWidget(self.kills_input)

        self.assists_label = QLabel("Assists:")
        layout.addWidget(self.assists_label)
        self.assists_input = QLineEdit()
        layout.addWidget(self.assists_input)

        self.deaths_label = QLabel("Deaths:")
        layout.addWidget(self.deaths_label)
        self.deaths_input = QLineEdit()
        layout.addWidget(self.deaths_input)

        self.kd_ratio_label = QLabel("K/D Ratio:")
        layout.addWidget(self.kd_ratio_label)
        self.kd_ratio_input = QLineEdit()
        layout.addWidget(self.kd_ratio_input)

        self.rating_label = QLabel("Rating 2.0:")
        layout.addWidget(self.rating_label)
        self.rating_input = QLineEdit()
        layout.addWidget(self.rating_input)

        self.notes_label = QLabel("Заметки:")
        layout.addWidget(self.notes_label)
        self.notes_input = QTextEdit()
        layout.addWidget(self.notes_input)

        self.submit_button = QPushButton("Добавить матч")
        self.submit_button.clicked.connect(self.log_match)
        layout.addWidget(self.submit_button)

    def log_match(self):
        date = self.date_input.date().toPyDate()
        official = self.official_input.currentText() == "Да"
        kills = int(self.kills_input.text())
        assists = int(self.assists_input.text())
        deaths = int(self.deaths_input.text())
        kd_ratio = float(self.kd_ratio_input.text())
        rating = float(self.rating_input.text())
        notes = self.notes_input.toPlainText()

        if not (self.kills_input.text() and self.assists_input.text() and self.deaths_input.text() and self.kd_ratio_input.text() and self.rating_input.text() and notes):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        Match.create(
            date=date,
            official=official,
            kills=kills,
            assists=assists,
            deaths=deaths,
            kd_ratio=kd_ratio,
            rating=rating,
            notes=notes
        )

        self.official_input.setCurrentIndex(0)
        self.kills_input.clear()
        self.assists_input.clear()
        self.deaths_input.clear()
        self.kd_ratio_input.clear()
        self.rating_input.clear()
        self.notes_input.clear()
        QMessageBox.information(self, "Успех", "Матч добавлен")

        self.match_added.emit()  # Испускание сигнала
