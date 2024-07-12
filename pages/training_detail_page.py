from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class TrainingDetailPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Здесь будут детали выбранной тренировки"))
        self.setLayout(layout)
