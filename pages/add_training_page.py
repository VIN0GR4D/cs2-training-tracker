from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox

class AddTrainingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Добавить тренировку"))

        layout.addWidget(QLabel("Выберите карту"))
        self.map_selector = QComboBox(self)
        self.map_selector.addItems(["Mirage", "Dust 2", "aim_botz"])
        layout.addWidget(self.map_selector)

        layout.addWidget(QLabel("Цель тренировки"))
        self.goal_selector = QComboBox(self)
        self.goal_selector.addItems(["Раскидка", "Аим"])
        layout.addWidget(self.goal_selector)

        layout.addWidget(QLabel("Описание тренировки"))
        self.description_input = QTextEdit(self)
        layout.addWidget(self.description_input)

        self.submit_button = QPushButton("Добавить тренировку", self)
        self.submit_button.clicked.connect(self.add_training)
        layout.addWidget(self.submit_button)

    def add_training(self):
        map_selected = self.map_selector.currentText()
        goal_selected = self.goal_selector.currentText()
        description = self.description_input.toPlainText()

        if not description:
            QMessageBox.warning(self, "Ошибка", "Описание не может быть пустым")
            return

        # Сюда добавить базу данных

        QMessageBox.information(self, "Тренировка добавлена", f"Карта: {map_selected}\nЦель: {goal_selected}\nОписание: {description}")

        self.map_selector.setCurrentIndex(0)
        self.goal_selector.setCurrentIndex(0)
        self.description_input.clear()
