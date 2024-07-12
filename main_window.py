from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QStackedWidget, QApplication, QStyle, QAction, QMenuBar, QMessageBox
from PyQt5.QtCore import Qt, QSize
from navigation_panel import NavigationPanel
from pages.training_list_page import TrainingListPage
from pages.matches_list_page import MatchesListPage
from pages.activity_chart_page import ActivityChartPage
from pages.add_training_page import AddTrainingPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CS2 Training Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Создание меню
        menu_bar = self.menuBar()

        # Создание меню "Файл"
        file_menu = menu_bar.addMenu("Файл")

        # Добавление действия в меню "Файл"
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Создание меню "О программе"
        about_menu = menu_bar.addMenu("О программе")

        # Добавление действия в меню "О программе"
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)

        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)

        # Создание панели навигации
        nav_buttons_widget = QWidget()
        nav_buttons_layout = QVBoxLayout(nav_buttons_widget)
        nav_buttons_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        nav_buttons_layout.setContentsMargins(0, 0, 0, 0)  # Удаление отступов
        nav_buttons_layout.setSpacing(0)  # Добавление расстояния между кнопками

        button_size = QSize(120, 40)  # Определение размера кнопки

        # Создание кнопок навигации
        btn_home = QToolButton(self)
        btn_home.setText("Главная")
        btn_home.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        btn_home.setIconSize(QSize(24, 24))  # Установка размера иконки
        btn_home.setFixedSize(button_size)
        btn_home.setStyleSheet("text-align: left;")  # Выравнивание текста по левому краю
        btn_home.clicked.connect(lambda: self.show_page(0))
        nav_buttons_layout.addWidget(btn_home)

        btn_add_training = QToolButton(self)
        btn_add_training.setText("Добавить тренировку")
        btn_add_training.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        btn_add_training.setIconSize(QSize(24, 24))  # Установка размера иконки
        btn_add_training.setFixedSize(button_size)
        btn_add_training.setStyleSheet("text-align: left;")  # Выравнивание текста по левому краю
        btn_add_training.clicked.connect(lambda: self.show_page(1))
        nav_buttons_layout.addWidget(btn_add_training)

        btn_training_list = QToolButton(self)
        btn_training_list.setText("Список тренировок")
        btn_training_list.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        btn_training_list.setIconSize(QSize(24, 24))  # Установка размера иконки
        btn_training_list.setFixedSize(button_size)
        btn_training_list.setStyleSheet("text-align: left;")  # Выравнивание текста по левому краю
        btn_training_list.clicked.connect(lambda: self.show_page(2))
        nav_buttons_layout.addWidget(btn_training_list)

        btn_add_match = QToolButton(self)
        btn_add_match.setText("Добавить матч")
        btn_add_match.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        btn_add_match.setIconSize(QSize(24, 24))  # Установка размера иконки
        btn_add_match.setFixedSize(button_size)
        btn_add_match.setStyleSheet("text-align: left;")  # Выравнивание текста по левому краю
        btn_add_match.clicked.connect(lambda: self.show_page(3))
        nav_buttons_layout.addWidget(btn_add_match)

        btn_match_list = QToolButton(self)
        btn_match_list.setText("Список матчей")
        btn_match_list.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        btn_match_list.setIconSize(QSize(24, 24))  # Установка размера иконки
        btn_match_list.setFixedSize(button_size)
        btn_match_list.setStyleSheet("text-align: left;")  # Выравнивание текста по левому краю
        btn_match_list.clicked.connect(lambda: self.show_page(4))
        nav_buttons_layout.addWidget(btn_match_list)

        btn_help = QToolButton(self)
        btn_help.setText("Справка")
        btn_help.setIcon(self.style().standardIcon(QStyle.SP_DialogHelpButton))
        btn_help.setIconSize(QSize(24, 24))  # Установка размера иконки
        btn_help.setFixedSize(button_size)
        btn_help.setStyleSheet("text-align: left;")  # Выравнивание текста по левому краю
        btn_help.clicked.connect(lambda: self.show_page(5))
        nav_buttons_layout.addWidget(btn_help)

        nav_buttons_layout.addStretch()

        # Создание stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(ActivityChartPage(self))  # Индекс 0 - Главная страница с графиком активности
        self.stacked_widget.addWidget(AddTrainingPage(self))  # Индекс 1 - Страница добавления тренировки
        self.stacked_widget.addWidget(TrainingListPage(self))  # Индекс 2 - Страница списка тренировок
        self.stacked_widget.addWidget(NavigationPanel(self))  # Индекс 3 - Страница добавления матча
        self.stacked_widget.addWidget(MatchesListPage(self))  # Индекс 4 - Страница списка матчей

        central_layout.addWidget(nav_buttons_widget, 0)
        central_layout.addWidget(self.stacked_widget, 1)

        self.setCentralWidget(central_widget)

    def show_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def show_about_dialog(self):
        QMessageBox.about(self, "О программе", "CS2 Training Tracker\nВерсия 1.0")

def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()

if __name__ == "__main__":
    main()
