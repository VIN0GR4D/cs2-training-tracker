import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from main_window import MainWindow

def main():
    # Удаление старой базы данных, если она существует и не используется
    if os.path.exists('trainings.db'):
        try:
            os.remove('trainings.db')
        except PermissionError:
            print("123.")

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
