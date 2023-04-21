from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session
from werkzeug.security import generate_password_hash

sql_database = "sqlite:///users.db"
engine = create_engine(sql_database)


# Определяем базовый класс моделей ORM для декларативной базы данных
class Base(DeclarativeBase):
    pass


# Создаем таблицу базы данных ORM и модель данных для таблицы
class Useer(Base):
    __tablename__ = "base_people"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    password = Column(String)
    name = Column(String)


# Создаем таблицы в базе данных, если их еще нет
Base.metadata.create_all(bind=engine)
# Создаем сессию ORM для выполнения операций в базе данных
db = Session(autoflush=False, bind=engine)


# Инициализируем базу данных начальными данными
def init():
    # Создаем объекты модели данных для начальных записей
    user_1 = Useer(user_name="Саша", password=generate_password_hash("Ignat", "sha256"), name="Cane")
    user_2 = Useer(user_name="Игорь", password=generate_password_hash("hgjdfjjsdksd", "sha256"), name="Игорь")
    list_1 = [user_1, user_2]
    # Добавляем объекты в сессию ORM и фиксируем изменения в базе данных
    db.add_all(list_1)
    db.commit()

# if __name__ == "__main__":
#     init()
