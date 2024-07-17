from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QStackedWidget, QStyle, QAction, QMenuBar, QMessageBox, QScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from navigation_panel import NavigationPanel
from pages.training_list_page import TrainingListPage
from pages.activity_chart_page import ActivityChartPage
from pages.add_training_page import AddTrainingPage
from pages.add_match_page import AddMatchPage
from pages.calendar_event_page import CalendarEventPage
from pages.matches_list_page import MatchesListPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Training Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Установка иконки окна
        self.setWindowIcon(QIcon('cs2-logo.png'))

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
        nav_buttons_layout.setContentsMargins(0, 0, 0, 0)
        nav_buttons_layout.setSpacing(0)

        button_size = QSize(120, 40)

        # Создание кнопок навигации
        btn_home = QToolButton(self)
        btn_home.setText("Главная")
        btn_home.setIcon(QIcon('home.png'))
        btn_home.setIconSize(QSize(24, 24))
        btn_home.setFixedSize(button_size)
        btn_home.setStyleSheet("text-align: left;")
        btn_home.clicked.connect(lambda: self.show_page(0))
        btn_home.setToolTip("Главная страница")
        nav_buttons_layout.addWidget(btn_home)

        btn_add_training = QToolButton(self)
        btn_add_training.setText("Добавить тренировку")
        btn_add_training.setIcon(QIcon('add.png'))
        btn_add_training.setIconSize(QSize(24, 24))
        btn_add_training.setFixedSize(button_size)
        btn_add_training.setStyleSheet("text-align: left;")
        btn_add_training.clicked.connect(lambda: self.show_page(1))
        btn_add_training.setToolTip("Добавить новую тренировку")
        nav_buttons_layout.addWidget(btn_add_training)

        btn_training_list = QToolButton(self)
        btn_training_list.setText("Список тренировок")
        btn_training_list.setIcon(QIcon('list.png'))
        btn_training_list.setIconSize(QSize(24, 24))
        btn_training_list.setFixedSize(button_size)
        btn_training_list.setStyleSheet("text-align: left;")
        btn_training_list.clicked.connect(lambda: self.show_page(2))
        btn_training_list.setToolTip("Просмотреть список всех тренировок")
        nav_buttons_layout.addWidget(btn_training_list)

        btn_add_match = QToolButton(self)
        btn_add_match.setText("Добавить матч")
        btn_add_match.setIcon(QIcon('add.png'))
        btn_add_match.setIconSize(QSize(24, 24))
        btn_add_match.setFixedSize(button_size)
        btn_add_match.setStyleSheet("text-align: left;")
        btn_add_match.clicked.connect(lambda: self.show_page(3))
        btn_add_match.setToolTip("Добавить новый матч")
        nav_buttons_layout.addWidget(btn_add_match)

        btn_match_list = QToolButton(self)
        btn_match_list.setText("Список матчей")
        btn_match_list.setIcon(QIcon('list.png'))
        btn_match_list.setIconSize(QSize(24, 24))
        btn_match_list.setFixedSize(button_size)
        btn_match_list.setStyleSheet("text-align: left;")
        btn_match_list.clicked.connect(lambda: self.show_page(4))
        btn_match_list.setToolTip("Просмотреть список всех матчей")
        nav_buttons_layout.addWidget(btn_match_list)

        btn_calendar_event = QToolButton(self)
        btn_calendar_event.setText("События календаря")
        btn_calendar_event.setIcon(QIcon('calendar.png'))
        btn_calendar_event.setIconSize(QSize(24, 24))
        btn_calendar_event.setFixedSize(button_size)
        btn_calendar_event.setStyleSheet("text-align: left;")
        btn_calendar_event.clicked.connect(lambda: self.show_page(5))
        btn_calendar_event.setToolTip("Просмотреть события календаря")
        nav_buttons_layout.addWidget(btn_calendar_event)

        btn_help = QToolButton(self)
        btn_help.setText("Справка")
        btn_help.setIcon(QIcon('help.png'))
        btn_help.setIconSize(QSize(24, 24))
        btn_help.setFixedSize(button_size)
        btn_help.setStyleSheet("text-align: left;")
        btn_help.clicked.connect(lambda: self.show_page(6))
        btn_help.setToolTip("Открыть справку")
        nav_buttons_layout.addWidget(btn_help)

        nav_buttons_layout.addStretch()

        # Создание stacked widget
        self.stacked_widget = QStackedWidget()
        self.activity_chart_page = ActivityChartPage(self)  # Индекс 0 - Главная страница с графиком активности
        self.add_training_page = AddTrainingPage(self)  # Индекс 1 - Страница добавления тренировки
        self.training_list_page = TrainingListPage(self)  # Индекс 2 - Страница списка тренировок
        self.add_match_page = AddMatchPage(self)  # Индекс 3 - Страница добавления матча
        self.matches_list_page = MatchesListPage(self)  # Индекс 4 - Страница списка матчей
        self.calendar_event_page = CalendarEventPage(self)  # Индекс 5 - Страница событий календаря

        self.stacked_widget.addWidget(self.activity_chart_page)
        self.stacked_widget.addWidget(self.add_training_page)
        self.stacked_widget.addWidget(self.training_list_page)
        self.stacked_widget.addWidget(self.add_match_page)  # Добавление страницы добавления матча
        self.stacked_widget.addWidget(self.matches_list_page)  # Добавление страницы списка матчей
        self.stacked_widget.addWidget(self.calendar_event_page)  # Добавление страницы событий календаря

        central_layout.addWidget(nav_buttons_widget, 0)
        central_layout.addWidget(self.stacked_widget, 1)

        self.setCentralWidget(central_widget)

        # Соединение сигнала из AddTrainingPage и AddMatchPage со слотом обновления списка в TrainingListPage и MatchesListPage
        self.add_training_page.training_added.connect(self.training_list_page.update_list)
        self.add_match_page.match_added.connect(self.matches_list_page.update_list)

    def show_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def show_about_dialog(self):
        QMessageBox.about(self, "О программе", "CS2 Training Tracker\nВерсия 1.0")
