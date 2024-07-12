from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from pages.training_list_page import TrainingListPage
from pages.training_detail_page import TrainingDetailPage
from pages.add_training_page import AddTrainingPage

class NavigationPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()

        self.training_list_page = TrainingListPage(self)
        self.training_detail_page = TrainingDetailPage(self)
        self.add_training_page = AddTrainingPage(self)

        self.stacked_widget.addWidget(self.training_list_page)
        self.stacked_widget.addWidget(self.training_detail_page)
        self.stacked_widget.addWidget(self.add_training_page)

        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)
