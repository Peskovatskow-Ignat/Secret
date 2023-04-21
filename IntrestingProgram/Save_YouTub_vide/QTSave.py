from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from pytube import YouTube
from PyQt5.QtWidgets import QProgressDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Задаем параметры окна
        self.setWindowTitle("Загрузчик YouTube")
        self.setGeometry(100, 100, 600, 300)
        self.setFixedSize(600, 300)
        self.setWindowIcon(QIcon('youtube.png'))

        # Задаем стиль для приложения
        style = """
        QMainWindow {
            background-color: #222;
        }
        QLabel {
            color: #fff;
        }
        QLineEdit {
            background-color: #555;
            color: #fff;
        }
        QComboBox {
            background-color: #555;
            color: #fff;
        }
        QPushButton {
            background-color: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #3E8E41;
        }
        """
        self.setStyleSheet(style)

        # Задаем шрифт для текста
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.setFont(font)

        # Добавляем виджеты на главное окно
        self.link_label = QLabel(self)
        self.link_label.setText("Ссылка на видео:")
        self.link_label.move(20, 20)

        self.link_input = QLineEdit(self)
        self.link_input.move(20, 50)
        self.link_input.resize(560, 30)

        self.quality_label = QLabel(self)
        self.quality_label.setText("Качество:")
        self.quality_label.move(20, 100)

        self.quality_combo = QComboBox(self)
        self.quality_combo.addItem("Высокое")
        self.quality_combo.addItem("Низкое")
        self.quality_combo.move(20, 130)
        self.quality_combo.resize(560, 30)

        self.download_button = QPushButton(self)
        self.download_button.setText("Загрузить видео")
        self.download_button.move(20, 190)
        self.download_button.resize(560, 40)
        self.download_button.clicked.connect(self.download_video)

    def download_video(self):
        link = self.link_input.text()
        try:
            video = YouTube(link)
        except:
            QMessageBox.critical(self, "Ошибка", "Недействительная ссылка на видео.")
            return

        quality = self.quality_combo.currentText()
        if quality == "Высокое":
            output = video.streams.get_highest_resolution()
        else:
            output = video.streams.get_lowest_resolution()

        try:
            output.download()
        except:
            QMessageBox.critical(self, "Ошибка", "Ошибка загрузки видео.")
            return

        QMessageBox.information(self, "Успех", "Загрузка завершена.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
