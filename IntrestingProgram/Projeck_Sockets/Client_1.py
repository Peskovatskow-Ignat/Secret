import sys
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
import socket
from threading import Thread
from time import sleep
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data = ""


class IPconnect(QDialog):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        uic.loadUi('ipclient.ui', self)
        self.setWindowTitle('ChatBobchat')
        self.createaccbutton.clicked.connect(lambda: self.ip_address())

    def ip_address(self):
        ip_address = self.password.text()
        self.password.setText('')
        print(ip_address)
        print(len(ip_address))
        if ip_address == '':
            print(0)
            return False
        print(len(ip_address))
        print(str(ip_address))
        self.sock.connect((ip_address, 55500))
        print(2)
        self.close()
        ex = Logup(self.sock)
        ex.show()
        sleep(1)


class Logup(QDialog):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        uic.loadUi('log_up.ui', self)
        self.setWindowTitle('ChatBobchat')
        self.LogupButton.clicked.connect(lambda: self.log_in())
        self.createaccbutton.clicked.connect(lambda: self.to_reg())
        self.password_2.setReadOnly(True)

    # Обработчик события для кнопки "Войти в систему"
    def log_in(self):
        # Очистка поля пароля для сообщения об ошибке
        self.password_2.setText('')
        # Получение введенных пользователем логина и пароля
        login = self.username_2.text()
        password = self.password.text()
        if login == "" or password == "":
            self.password_2.setText("Заполните все поля")
            return False
        # Отправка кода операции (1 - вход в систему) на сервер
        sock.send("1".encode())
        # Очистка полей логина и пароля
        self.username_2.setText('')
        self.password.setText('')
        # Отправка логина и пароля на сервер
        sock.send(login.encode())
        sleep(0.1)
        sock.send(password.encode())
        # Получение ответа от сервера
        response = sock.recv(1024).decode()
        # Отображение ответа сервера в поле для сообщений об ошибке
        self.password_2.setText(response)
        # Если ответ сервера содержит "Успешно", закрытие текущего окна и открытие окна чата
        if "Успешно" in response:
            self.close()
            ex = Chat(self.sock)
            ex.show()
            sleep(1)

    # Обработчик события для кнопки "Создать аккаунт"
    def to_reg(self):
        # Закрытие текущего окна и открытие окна регистрации
        self.close()
        ex = Reg(self.sock)
        ex.show()


class Reg(QDialog):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        uic.loadUi('registrations.ui', self)
        self.setWindowTitle('ChatBobchat')
        self.LogupButton.clicked.connect(lambda: self.registers())
        self.createaccbutton.clicked.connect(lambda: self.to_log())
        self.password_2.setReadOnly(True)

        # Метод регистрации нового пользователя

    def registers(self):
        # Очищаем поле для ввода подтверждения пароля
        self.password_2.setText('')
        # Считываем введенные пользователем данные (логин, пароль, имя)
        login = self.username_2.text()
        password = self.password.text()
        name = self.password_3.text()
        if login == "" or password == "" or name == "":
            self.password_2.setText("Заполните все поля")
            return False
        # Отправляем на сервер сообщение о том, что это запрос на регистрацию
        sock.send("2".encode())
        # Очищаем поля для ввода
        self.username_2.setText('')
        self.password.setText('')
        self.password_3.setText('')
        # Отправляем на сервер введенные пользователем данные
        sock.send(login.encode())
        sleep(0.1)
        sock.send(password.encode())
        sleep(0.1)
        sock.send(name.encode())
        # Получаем ответ от сервера и выводим его в поле для ввода подтверждения пароля
        response = sock.recv(1024).decode()
        self.password_2.setText(response)
        # Если регистрация прошла успешно, закрываем окно регистрации и открываем окно входа
        if "Успешно" in response:
            self.close()
            ex = Logup(self.sock)
            ex.show()

    # Обработчик события для кнопки "Войти"
    def to_log(self):
        # Закрытие текущего окна и открытие окна Входа
        self.close()
        ex = Logup(self.sock)
        ex.show()


class Chat(QDialog):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        uic.loadUi('chat.ui', self)
        self.setWindowTitle('ChatBobchat')
        self.createaccbutton.clicked.connect(lambda: self.send_message())
        self.textBrowser.setReadOnly(True)
        self.password_2.setReadOnly(True)
        th = Thread(target=self.get_message, daemon=True)
        th.start()

    def get_message(self):
        while True:
            messages = sock.recv(1024).decode().split(';')
            active_users = messages[0]
            sleep(0.1)
            if not messages:
                sleep(0.1)
                continue
            try:
                self.textBrowser.append(messages[1])
                self.password_2.setText('')
                self.password_2.setText(active_users)
            except Exception as e:
                print(e)

    def send_message(self):
        message = self.password.text()
        sleep(0.1)
        data = datetime.now().strftime("%Y-%m-%d %H:%M")
        end = f"""{data}
{message}"""
        if message == "":
            clown = "Я клоун 🤡"
            sleep(0.1)
            sock.send(clown.encode('utf-8'))
        else:
            sock.send(end.encode('utf-8'))
            sleep(0.1)
            self.password.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IPconnect(sock)
    ex.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        sock.send("Покидает чат👋".encode())
        print("...")
        sock.close()
