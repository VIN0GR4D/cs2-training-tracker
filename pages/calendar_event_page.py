from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget, QPushButton, QDialog, QFormLayout, QLineEdit, QTextEdit, QDialogButtonBox
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor
from peewee import SqliteDatabase, Model, DateField, CharField, TextField
import datetime

db = SqliteDatabase('trainings.db')

class CalendarEvent(Model):
    date = DateField()
    event_type = CharField()
    description = TextField()

    class Meta:
        database = db

db.connect()
db.create_tables([CalendarEvent])

class AddEventDialog(QDialog):
    event_added = pyqtSignal()  # Сигнал, который испускается при добавлении события

    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date
        self.setWindowTitle("Добавить событие")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        self.event_type_input = QLineEdit(self)
        layout.addRow("Тип события:", self.event_type_input)

        self.description_input = QTextEdit(self)
        layout.addRow("Описание:", self.description_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def get_event_data(self):
        event_type = self.event_type_input.text()
        description = self.description_input.toPlainText()

        return {
            "event_type": event_type,
            "description": description,
            "date": self.date.toPyDate()  # Преобразование QDate в datetime.date
        }

    def accept(self):
        data = self.get_event_data()
        CalendarEvent.create(
            date=data["date"],
            event_type=data["event_type"],
            description=data["description"]
        )
        self.event_added.emit()  # Испускание сигнала
        super().accept()

class CalendarEventPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.show_events)
        layout.addWidget(self.calendar)

        self.events_label = QLabel("События на выбранный день:")
        layout.addWidget(self.events_label)

        self.add_event_button = QPushButton("Добавить событие", self)
        self.add_event_button.clicked.connect(self.open_add_event_dialog)
        layout.addWidget(self.add_event_button)

        self.refresh_calendar()

    def refresh_calendar(self):
        self.show_events(self.calendar.selectedDate())
        self.highlight_event_days()

    def show_events(self, date):
        events = CalendarEvent.select().where(CalendarEvent.date == date.toPyDate())
        events_text = [f"{event.event_type}: {event.description}" for event in events]
        self.events_label.setText("События на выбранный день:\n" + "\n".join(events_text))

    def open_add_event_dialog(self):
        selected_date = self.calendar.selectedDate()
        dialog = AddEventDialog(selected_date, self)
        dialog.event_added.connect(self.refresh_calendar)
        dialog.exec_()

    def highlight_event_days(self):
        # Сброс всех форматирований
        default_format = QTextCharFormat()
        self.calendar.setDateTextFormat(QDate(), default_format)

        # Получение всех уникальных дат с событиями
        event_dates = CalendarEvent.select(CalendarEvent.date).distinct()
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QBrush(QColor("green")))

        for event in event_dates:
            qdate = QDate(event.date.year, event.date.month, event.date.day)
            self.calendar.setDateTextFormat(qdate, highlight_format)
