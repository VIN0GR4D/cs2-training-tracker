from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from peewee import SqliteDatabase, Model, DateField, CharField, TextField

db = SqliteDatabase('trainings.db')

class Training(Model):
    date = DateField()
    map = CharField()
    goal = CharField()
    description = TextField()

    class Meta:
        database = db

class TrainingListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.update_list()

    def update_list(self):
        # Очистка текущего списка
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        self.layout.addWidget(QLabel("Список тренировок:"))

        # Получение списка тренировок из базы данных
        trainings = Training.select()
        for training in trainings:
            training_frame = QFrame()
            training_frame.setFrameShape(QFrame.Box)
            training_frame.setFrameShadow(QFrame.Raised)
            training_layout = QVBoxLayout()

            date_label = QLabel(f"Дата: {training.date}")
            map_label = QLabel(f"Карта: {training.map}")
            goal_label = QLabel(f"Цель: {training.goal}")
            description_label = QLabel(f"Описание: {training.description}")

            training_layout.addWidget(date_label)
            training_layout.addWidget(map_label)
            training_layout.addWidget(goal_label)
            training_layout.addWidget(description_label)

            training_frame.setLayout(training_layout)
            training_frame.setStyleSheet("QFrame { margin: 10px; padding: 5px; } QLabel { margin: 2px; }")

            self.layout.addWidget(training_frame)
