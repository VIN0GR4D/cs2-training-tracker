from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtCore import QDate, pyqtSignal
from peewee import SqliteDatabase, Model, DateField, CharField, TextField

db = SqliteDatabase('trainings.db')

class Training(Model):
    date = DateField()
    map = CharField()
    goal = CharField()
    description = TextField()

    class Meta:
        database = db

db.connect()
db.create_tables([Training], safe=True)

class AddTrainingPage(QWidget):
    training_added = pyqtSignal()  # Сигнал, который испускается при добавлении тренировки

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

        self.map_label = QLabel("Карта:")
        layout.addWidget(self.map_label)
        self.map_input = QComboBox()
        self.map_input.addItems(["Mirage", "Dust 2", "aim_botz"])
        layout.addWidget(self.map_input)

        self.goal_label = QLabel("Цель тренировки:")
        layout.addWidget(self.goal_label)
        self.goal_input = QComboBox()
        self.goal_input.addItems(["Раскидка", "Аим"])
        layout.addWidget(self.goal_input)

        self.description_label = QLabel("Описание:")
        layout.addWidget(self.description_label)
        self.description_input = QTextEdit()
        layout.addWidget(self.description_input)

        self.submit_button = QPushButton("Добавить тренировку")
        self.submit_button.clicked.connect(self.log_training)
        layout.addWidget(self.submit_button)

    def log_training(self):
        date = self.date_input.date().toPyDate()
        map = self.map_input.currentText()
        goal = self.goal_input.currentText()
        description = self.description_input.toPlainText()

        if not description:
            QMessageBox.warning(self, "Ошибка", "Описание не может быть пустым")
            return

        Training.create(date=date, map=map, goal=goal, description=description)

        self.map_input.setCurrentIndex(0)
        self.goal_input.setCurrentIndex(0)
        self.description_input.clear()
        QMessageBox.information(self, "Успех", "Тренировка добавлена")

        self.training_added.emit()  # Испускание сигнала
