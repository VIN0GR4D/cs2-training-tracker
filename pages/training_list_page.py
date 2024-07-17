from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QSizePolicy, QPushButton, QMessageBox, QMenu, QToolButton
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
        self.layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(QLabel("Список тренировок:"))
        self.layout.addWidget(self.scroll_area)

        self.update_list()

    def update_list(self):
        # Очистка текущего списка
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

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

            # Создание кнопки с выпадающим меню
            action_button = QToolButton()
            action_button.setText("Действия")
            action_button.setPopupMode(QToolButton.InstantPopup)
            menu = QMenu(action_button)
            delete_action = menu.addAction("Удалить")
            delete_action.triggered.connect(lambda _, t=training: self.delete_training(t))
            action_button.setMenu(menu)

            training_layout.addWidget(date_label)
            training_layout.addWidget(map_label)
            training_layout.addWidget(goal_label)
            training_layout.addWidget(description_label)
            training_layout.addWidget(action_button)

            training_frame.setLayout(training_layout)
            training_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            training_frame.setStyleSheet("QFrame { margin: 5px; padding: 5px; } QLabel { margin: 1px; }")

            self.scroll_layout.addWidget(training_frame)

    def delete_training(self, training):
        confirm = QMessageBox.question(self, "Подтверждение удаления", "Вы уверены, что хотите удалить эту тренировку?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            training.delete_instance()
            self.update_list()
