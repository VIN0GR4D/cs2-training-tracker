from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtCore import QDate, pyqtSignal
from peewee import SqliteDatabase, Model, DateField, CharField, TextField, BooleanField

db = SqliteDatabase('trainings.db')

class Match(Model):
    date = DateField()
    official = BooleanField()
    stats = CharField()
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

        self.stats_label = QLabel("Личная статистика:")
        layout.addWidget(self.stats_label)
        self.stats_input = QLineEdit()
        layout.addWidget(self.stats_input)

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
        stats = self.stats_input.text()
        notes = self.notes_input.toPlainText()

        if not stats or not notes:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        Match.create(date=date, official=official, stats=stats, notes=notes)

        self.official_input.setCurrentIndex(0)
        self.stats_input.clear()
        self.notes_input.clear()
        QMessageBox.information(self, "Успех", "Матч добавлен")

        self.match_added.emit()  # Испускание сигнала
