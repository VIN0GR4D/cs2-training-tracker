from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QHBoxLayout, QSizePolicy, QMessageBox, QMenu, QToolButton, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from peewee import SqliteDatabase, Model, DateField, BooleanField, IntegerField, FloatField, TextField

db = SqliteDatabase('trainings.db')

class Match(Model):
    date = DateField()
    official = BooleanField()
    kills = IntegerField()
    assists = IntegerField()
    deaths = IntegerField()
    kd_ratio = FloatField()
    rating = FloatField()
    notes = TextField()

    class Meta:
        database = db

class MatchesListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(QLabel("Список матчей:"))
        self.layout.addWidget(self.scroll_area)

        # Заголовок таблицы
        header_frame = QFrame()
        header_layout = QGridLayout(header_frame)
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(0, 0, 0, 0)

        headers = ["Date", "Map", "Score", "Kills", "Assists", "Deaths", "+/-", "Rating 2.0", "Actions"]
        column_widths = [80, 100, 80, 80, 80, 80, 80, 80, 50]  # Устанавливаем фиксированную ширину для каждой колонки

        for i, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("color: #ffffff; font-weight: bold;")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(column_widths[i])
            header_layout.addWidget(label, 0, i)

        header_frame.setLayout(header_layout)
        header_frame.setStyleSheet("background-color: #444; padding: 0px; margin-bottom: 0px;")
        header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_layout.addWidget(header_frame, alignment=Qt.AlignTop)

        self.map_images = {
            "Dust2": "images/Dust2.jpg",
            "Mirage": "images/Mirage.jpg",
            "Inferno": "images/Inferno.jpg",
            "Nuke": "images/Nuke.jpg",
            "Vertigo": "images/Vertigo.jpg",
            "Ancient": "images/Ancient.jpg",
            "Anubis": "images/Anubis.jpg",
        }

        self.update_list()

    def update_list(self):
        # Очистка текущего списка
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget and widget != self.scroll_layout.itemAt(0).widget():
                widget.setParent(None)

        # Получение списка матчей из базы данных
        matches = Match.select()
        for match in matches:
            match_frame = QFrame()
            match_frame.setFrameShape(QFrame.NoFrame)
            match_frame.setStyleSheet("""
                QFrame {
                    background-color: #333;
                    margin: 5px 0px;
                    padding: 5px;
                }
            """)
            match_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            match_layout = QGridLayout(match_frame)
            match_layout.setSpacing(0)
            match_layout.setContentsMargins(0, 0, 0, 0)

            # Колонка даты
            date_label = QLabel(match.date.strftime("%d %b"))
            date_label.setStyleSheet("color: #fff;")
            date_label.setAlignment(Qt.AlignCenter)
            date_label.setFixedWidth(80)
            match_layout.addWidget(date_label, 0, 0)

            # Колонка карты с изображением
            map_label = QLabel()
            pixmap = QPixmap(self.map_images.get(match.notes, ""))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                map_label.setPixmap(pixmap)
            map_label.setAlignment(Qt.AlignCenter)
            map_label.setFixedWidth(100)
            match_layout.addWidget(map_label, 0, 1)

            # Колонка счета
            score_label = QLabel(f"{match.kills} / {match.deaths}")
            score_label.setStyleSheet("color: #0f0;" if match.kd_ratio > 1 else "color: #f00;")
            score_label.setAlignment(Qt.AlignCenter)
            score_label.setFixedWidth(80)
            match_layout.addWidget(score_label, 0, 2)

            # Колонка убийств
            kills_label = QLabel(str(match.kills))
            kills_label.setStyleSheet("color: #fff;")
            kills_label.setAlignment(Qt.AlignCenter)
            kills_label.setFixedWidth(80)
            match_layout.addWidget(kills_label, 0, 3)

            # Колонка ассистов
            assists_label = QLabel(str(match.assists))
            assists_label.setStyleSheet("color: #fff;")
            assists_label.setAlignment(Qt.AlignCenter)
            assists_label.setFixedWidth(80)
            match_layout.addWidget(assists_label, 0, 4)

            # Колонка смертей
            deaths_label = QLabel(str(match.deaths))
            deaths_label.setStyleSheet("color: #fff;")
            deaths_label.setAlignment(Qt.AlignCenter)
            deaths_label.setFixedWidth(80)
            match_layout.addWidget(deaths_label, 0, 5)

            # Колонка +/-
            plus_minus = match.kills - match.deaths
            plus_minus_label = QLabel(str(plus_minus))
            if plus_minus > 0:
                plus_minus_label.setStyleSheet("color: #0f0;")
            elif plus_minus < 0:
                plus_minus_label.setStyleSheet("color: #f00;")
            else:
                plus_minus_label.setStyleSheet("color: #aaa;")
            plus_minus_label.setAlignment(Qt.AlignCenter)
            plus_minus_label.setFixedWidth(80)


            # Колонка рейтинга
            rating_label = QLabel(f"{match.rating:.2f}")
            rating_label.setStyleSheet("color: #fff;")
            rating_label.setAlignment(Qt.AlignCenter)
            rating_label.setFixedWidth(80)
            match_layout.addWidget(rating_label, 0, 7)

            # Кнопка с действиями (удаление и другие действия)
            action_button = QToolButton()
            action_button.setText("⋮")
            action_button.setStyleSheet("color: #fff; background-color: #444;")
            action_button.setPopupMode(QToolButton.InstantPopup)
            action_button.setToolButtonStyle(Qt.ToolButtonTextOnly)
            action_button.setFixedWidth(50)

            # Меню действий
            menu = QMenu(action_button)
            delete_action = menu.addAction("Удалить")
            delete_action.triggered.connect(lambda _, m=match: self.delete_match(m))
            favorite_action = menu.addAction("Добавить в избранное")
            action_button.setMenu(menu)

            match_layout.addWidget(action_button, 0, 8)

            match_frame.setLayout(match_layout)
            self.scroll_layout.addWidget(match_frame, alignment=Qt.AlignTop)

    def delete_match(self, match):
        confirm = QMessageBox.question(self, "Подтверждение удаления", "Вы уверены, что хотите удалить этот матч?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            match.delete_instance()
            self.update_list()
