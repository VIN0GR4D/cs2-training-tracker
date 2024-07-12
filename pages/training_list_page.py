from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class TrainingListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Здесь будет список тренировок"))
        self.setLayout(layout)
