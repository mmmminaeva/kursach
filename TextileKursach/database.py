import os
import sys

from PyQt6.QtSql import QSqlQuery, QSqlDatabase


def db_connect(db_name: str, new_db: bool = False) -> QSqlDatabase:
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)
    query = QSqlQuery()

    if not db.open():
        print(f"Database Error: {db.lastError().databaseText()}")
        sys.exit(1)

    query.exec('''create table if not exists User
        (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            login    varchar(255),
            password varchar(255),
            role varchar(255)
    );''')
    query.exec('''create table if not exists Cloth
        (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         VARCHAR(255),
            req_material DECIMAL(12, 2),
            req_time     DECIMAL(12, 2)
        );''')
    query.exec('''create table if not exists Material
        (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  VARCHAR(255),
            price DECIMAL(12, 2)
        );''')
    query.exec('''create table if not exists Status
        (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  VARCHAR(255)
        );''')
    query.exec('''create table if not exists Orders
        (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            User_id     INTEGER REFERENCES User (id),
            Cloth_id    INTEGER REFERENCES Cloth (id),
            Material_id INTEGER REFERENCES Material (id),
            status INTEGER REFERENCES Status(id),
            quantity    INTEGER,
            amount DECIMAL(16, 2),
            time DECIMAL(12, 2)
        );''')
    if new_db:
        query.exec('''drop table if exists User''')
        query.exec('''drop table if exists Status''')
        query.exec('''drop table if exists Cloth''')
        query.exec('''drop table if exists Material''')
        query.exec('''create table if not exists User
        (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            login    varchar(255),
            password varchar(255),
            role varchar(255)
        );''')
        query.exec('''create table if not exists Status
        (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  VARCHAR(255)
        );''')
        query.exec('''create table if not exists Cloth
            (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         VARCHAR(255),
                req_material DECIMAL(12, 2),
                req_time     DECIMAL(12, 2)
            );''')
        query.exec('''create table if not exists Material
            (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  VARCHAR(255),
                price DECIMAL(12, 2)
            );''')
        query.exec('''insert into User(id, login, password, role)
            values
            (1, 'admin', 'admin', 'admin'),
            (2, 'user', 'user', 'user');''')
        query.exec('''insert into Status(id, name)
            values
            (1, 'Принят'),
            (2, 'В процессе'),
            (3, 'Готов');
            ''')
        query.exec('''insert into Cloth (id, name, req_material, req_time)
            values 
            (1, 'Платье', 1.5, 2.0),
            (2, 'Сарафан', 2.0, 2.5),
            (3, 'Рубашка', 1.0, 1.5),
            (4, 'Юбка', 1.2, 1.0),
            (5, 'Брюки', 1.5, 2.0),
            (6, 'Пальто', 2.5, 3.5
            );''')
        query.exec('''insert into Material (id, name, price)
            values
            (1, 'Хлопок', 100.0),
            (2, 'Лен', 150.0),
            (3, 'Шерсть', 200.0),
            (4, 'Шифон', 120.0),
            (5, 'Бархат', 180.0),
            (6, 'Твид', 240.0);''')

    return db


if os.path.exists('Textile.sqlite'):
    db = db_connect('Textile.sqlite')
else:
    db = db_connect('Textile.sqlite', new_db=True)