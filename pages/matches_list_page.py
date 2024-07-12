from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class MatchesListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Здесь будет список матчей"))
        self.setLayout(layout)
