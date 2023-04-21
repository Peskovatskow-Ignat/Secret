from werkzeug.security import generate_password_hash, check_password_hash
from time import sleep
from database_users import Useer, db


def get_info():
    # Получаем информацию о всех пользователях из базы данных
    for i in db.query(Useer).all():
        print(f"ID: {i.id}, user_name: {i.user_name}, password: {i.password}")


def log_in(login, password, name):
    # Проверяем, занято ли имя пользователя в базе данных
    for check in db.query(Useer).all():
        if check.user_name == login:
            print("Пользователь с таким логином уже существует")
            return False
    # Если имя пользователя не занято, создаем нового пользователя в базе данных
    password_hash = generate_password_hash(password, "sha256")
    new_user = Useer(user_name=login, password=password_hash, name=name)
    db.add(new_user)
    db.commit()
    return name


# Функция для авторизации пользователя
def entrance(login, password):
    try:
        user = db.query(Useer).filter(Useer.user_name == login).first()
        if check_password_hash(user.password, password):
            print(f"Пользователь {user.name} Успешно авторизовался")
            return user.name
        else:
            print("Неверный пароль")
    except:
        print("Неверный логин")


# Функция для вывода меню и обработки выбора пользователя
def menu():
    print("-" * 80)
    print("... Вывести всех пользователей с паролями")
    print("-" * 80)
    choice = input("Выберите действие: ")
    if choice == "test":
        get_info()
        sleep(5)
        menu()
    else:
        db.close()


if __name__ == "__main__":
    menu()
