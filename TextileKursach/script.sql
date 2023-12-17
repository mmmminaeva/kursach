create table if not exists User
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    login    varchar(255),
    password varchar(255),
    role     varchar(255)
);

create table if not exists Cloth
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         VARCHAR(255),
    req_material DECIMAL(12, 2),
    req_time     DECIMAL(12, 2)
);

create table if not exists Material
(
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  VARCHAR(255),
    price DECIMAL(12, 2)
);

create table if not exists Orders
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    User_id     INTEGER REFERENCES User (id),
    Cloth_id    INTEGER REFERENCES Cloth (id),
    Material_id INTEGER REFERENCES Material (id),
    status INTEGER REFERENCES Status(id),
    quantity    INTEGER,
    amount DECIMAL(16, 2),
    time DECIMAL(12, 2)
);

-- Добавляет аккаунт для админа

insert into User(id, login, password, role)
values (1, 'admin', 'admin', 'admin');

-- Заполняем таблицу Cloth

insert into Cloth (id, name, req_material, req_time)
values (1, 'Платье', 1.5, 2.0),
       (2, 'Сарафан', 2.0, 2.5),
       (3, 'Рубашка', 1.0, 1.5),
       (4, 'Юбка', 1.2, 1.0),
       (5, 'Брюки', 1.5, 2.0),
       (6, 'Пальто', 2.5, 3.5);

-- Заполняем таблицу Material

insert into Material (id, name, price)
values (1, 'Хлопок', 100.0),
       (2, 'Лен', 150.0),
       (3, 'Шерсть', 200.0),
       (4, 'Шифон', 120.0),
       (5, 'Бархат', 180.0),
       (6, 'Твид', 240.0);

-- Заполняем таблицу Orders

insert into Orders (id, User_id, Cloth_id, Material_id, quantity, amount, time, status)
values (1, 2, 1, 6, 2, 1000.0, 15.5, 1),
       (2, 2, 2, 5, 3, 1000.0, 15.5, 2),
       (3, 2, 3, 4, 1, 1000.0, 15.5, 3),
       (4, 2, 4, 3, 2, 1000.0, 15.5, 1),
       (5, 2, 5, 2, 3, 1000.0, 15.5, 2),
       (6, 2, 6, 1, 1, 1000.0, 15.5, 3);
