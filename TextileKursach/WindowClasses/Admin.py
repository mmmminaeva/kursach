from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QTableWidgetItem, QMainWindow

from UI_Files.AdminWindow_UI import Ui_MainWindow as AdminWin_UI
from WindowClasses.functions import show_message
from database import db


class AdminWindow(QMainWindow, AdminWin_UI):
    def __init__(self):
        super().__init__()
        self.ui = AdminWin_UI()
        self.ui.setupUi(self)
        self.setWindowTitle('Окно админа')

        self.results: list[list] = []

        self.db = db
        self.query: QSqlQuery = QSqlQuery(db)

        self.refresh_tables()

        self.ui.tabWidget.tabBarClicked.connect(self.refresh_tables)
        self.ui.add_material_btn.clicked.connect(self.addMaterial)
        self.ui.add_cloth_btn.clicked.connect(self.addCloth)
        self.ui.accepted_btn.clicked.connect(lambda:self.change_status(1))
        self.ui.in_process_btn.clicked.connect(lambda:self.change_status(2))
        self.ui.ready_btn.clicked.connect(lambda:self.change_status(3))

    def refresh_tables(self):
        self.select_orders()
        self.select_materials()
        self.select_clothes()

    def select_orders(self):
        self.results.clear()
        self.ui.tableWidget.clear()
        # Получение результата запроса
        self.query.exec(f"""select O.id, C.name Одежда, M.name Материал, O.quantity Количество,
                        O.amount Стоимость, O.time Время, S.name Статус
                        from Orders O
                        join Cloth C on C.id = O.Cloth_id
                        join Material M on M.id = O.Material_id
                        join Status S on S.id = O.status
                        join User U on U.id = O.User_id;""")

        id, cloth, material, quantity, amount, time, status = range(7)

        while self.query.next():
            self.results.append([self.query.value(id), self.query.value(cloth), self.query.value(material),
                                 self.query.value(quantity), self.query.value(amount),
                                 self.query.value(time), self.query.value(status)])

        # Количество столбцов и строк
        if not self.results or not len(self.results[0]):
            return

        row = len(self.results)
        col = len(self.results[0])
        self.ui.tableWidget.setRowCount(row)
        self.ui.tableWidget.setColumnCount(col)

        # Заголовок
        column_headers = ['Ид','Одежда', 'Материал', 'Количество', 'Стоимость', 'Время', 'Статус']
        self.ui.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        # Заполнение таблицы
        for row, result in enumerate(self.results):
            for column, value in enumerate(result):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(row, column, item)

        # Изменение размеров строк и столбцов
        self.ui.tableWidget.resizeColumnsToContents()

    def select_materials(self):
        self.results.clear()
        self.ui.tableWidget_4.clear()
        # Получение результата запроса
        self.query.exec(f"""select name, price from Material;""")

        name, price = range(2)

        while self.query.next():
            self.results.append([self.query.value(name), self.query.value(price)])

        # Количество столбцов и строк
        if not self.results or not len(self.results[0]):
            return

        row = len(self.results)
        col = len(self.results[0])
        self.ui.tableWidget_4.setRowCount(row)
        self.ui.tableWidget_4.setColumnCount(col)

        # Заголовок
        column_headers = ['Материал', 'Цена(руб.)']
        self.ui.tableWidget_4.setHorizontalHeaderLabels(column_headers)
        self.ui.tableWidget_4.horizontalHeader().setStretchLastSection(True)

        # Заполнение таблицы
        for row, result in enumerate(self.results):
            for column, value in enumerate(result):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget_4.setItem(row, column, item)

        # Изменение размеров строк и столбцов
        self.ui.tableWidget_4.resizeColumnsToContents()

    def select_clothes(self):
        self.results.clear()
        self.ui.tableWidget_3.clear()
        # Получение результата запроса
        self.query.exec(f"""select name, req_time, req_material from Cloth;""")

        name, req_time, req_material = range(3)

        while self.query.next():
            self.results.append([self.query.value(name), round(self.query.value(req_time),2),
                                 round(self.query.value(req_material),2)])

        # Количество столбцов и строк
        if not self.results or not len(self.results[0]):
            return

        row = len(self.results)
        col = len(self.results[0])
        self.ui.tableWidget_3.setRowCount(row)
        self.ui.tableWidget_3.setColumnCount(col)

        # Заголовок
        column_headers = ['Одежда', 'Время(ч.)', 'Материал(кв.м.)']
        self.ui.tableWidget_3.setHorizontalHeaderLabels(column_headers)
        self.ui.tableWidget_3.horizontalHeader().setStretchLastSection(True)

        # Заполнение таблицы
        for row, result in enumerate(self.results):
            for column, value in enumerate(result):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget_3.setItem(row, column, item)

        # Изменение размеров строк и столбцов
        self.ui.tableWidget_3.resizeColumnsToContents()

    def addMaterial(self):
        name = self.ui.material_le.text()
        price = self.ui.material_price_sb.value()

        self.query.exec(f"""insert into Material(name, price)
                            values ('{name}', {price});""")
        show_message(self, 'Успешно!', "Материал успешно добавлен!      ")

    def addCloth(self):
        name = self.ui.cloth_le.text()
        req_material = self.ui.req_material_sb.value()
        req_time = self.ui.req_time_sb.value()

        self.query.exec(f"""insert into Cloth(name, req_material, req_time)
                            values ('{name}', {req_material}, {req_time});""")
        show_message(self, 'Успешно!', "Одежда успешно добавлена!         ")

    def change_status(self, status_id):
        cur_row = self.ui.tableWidget.currentRow()
        if self.ui.tableWidget.item(cur_row, 0):
            cur_id = int(self.ui.tableWidget.item(cur_row, 0).text())
            self.query.exec(f'''update Orders
                                set status = {status_id}
                                where id = {cur_id}''')
            self.refresh_tables()
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

