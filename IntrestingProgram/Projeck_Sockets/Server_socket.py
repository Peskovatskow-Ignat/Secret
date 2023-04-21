import socket
from concurrent.futures import ThreadPoolExecutor
from database_select import entrance, log_in
from time import sleep

client_sockets = set()
list_users = set()
# Получаем локальный IP-адрес сервера
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Локальный IP: {local_ip}")

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 55500))
sock.listen(10)


# def rul(conn):
#     # Функция для отправки пользователю списка доступных действий
#     rules = ("-" * 80 + "\n" +
#              "1 - Войти в аккаунт" + "\n" +
#              "2 - Зарегестрироваться" + "\n" +
#              "... Вывести всех пользователей с паролями" + "\n" +
#              "-" * 80)
#     conn.send(rules.encode())


def rec(cs, address):
    # Функция для получения сообщений от клиента
    while True:
        try:
            sleep(0.1)
            message = cs.recv(1024).decode()
            sleep(0.1)
            if message == "Покидает чат👋":
                list_users.remove(address)
                client_sockets.remove(cs)
                cs.close()
        except Exception as error:
            print(error)
            # Если возникла ошибка при получении сообщения, удаляем сокет клиента
            client_sockets.remove(cs)
            list_users.remove(address)
            cs.close()
        else:
            user_string = " ".join(list_users)
            # Отправляем полученное сообщение всем клиентам, кроме отправителя
            for i in client_sockets:
                i.send(bytes(f"{user_string};{address}: {message}".encode()))


def con(conn, address):
    # Функция для обработки соединения с клиентом
    while True:
        register = conn.recv(1024).decode()
        if register == "1":
            # Если пользователь хочет войти в аккаунт, получаем от него логин и пароль
            login = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
            # Вызываем функцию entrance из модуля database_select для проверки данных пользователя
            if name := entrance(login, password):
                # Если данные верны, отправляем клиенту сообщение об успешной авторизации
                response = f"Пользователь {name} Успешно авторизовался"
                conn.send(response.encode())
                # Добавляем сокет клиента в множество
                user_name = name
                list_users.add(user_name)
                client_sockets.add(conn)
                break
            else:
                # Если данные неверны, отправляем клиенту сообщение об ошибке
                conn.send("Неверный логин или пароль".encode())

        if register == "2":
            # Если пользователь хочет зарегистрироваться, получаем от него логин, пароль и имя
            login = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
            name = conn.recv(1024).decode()
            # Вызываем функцию log_in из модуля database_select для добавления нового пользователя в базу данных
            if name := log_in(login, password, name):
                # Если регистрация прошла успешно, отправляем клиенту сообщение об успешной регистрации
                response = f"Пользователь {name} Успешно зарегистрировался"
                conn.send(response.encode())
                print(response)
            else:
                response = "Имя пользователя занято"
                conn.send(response.encode())
    rec(conn, user_name)


print("Server start")


# Функция для обработки входящих соединений от клиентов
def accept_client(server_sock):
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            client_conn, client_address = server_sock.accept()
            print(f"Connected from {client_address}")
            executor.submit(con, client_conn, client_address)


# Запускаем прослушивание входящих соединений в отдельном потоке
while True:
    accept_client(sock)
