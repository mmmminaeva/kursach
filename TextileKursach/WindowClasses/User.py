import openpyxl
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QTableWidgetItem, QMainWindow

from UI_Files.UserWindow_UI import Ui_MainWindow as UserWin_UI
from WindowClasses.functions import show_message
from database import db


class UserWindow(QMainWindow, UserWin_UI):
    def __init__(self, login):
        super().__init__()
        self.ui = UserWin_UI()
        self.ui.setupUi(self)
        self.setWindowTitle('Окно пользователя')

        self.results: list[list] = []
        self.login = login

        self.db = db
        self.query: QSqlQuery = QSqlQuery(db)

        self.setupTab()
        self.select()

        self.ui.tabWidget.tabBarClicked.connect(self.select)
        self.ui.export_btn.clicked.connect(self.export_table)
        self.ui.calculate_btn.clicked.connect(self.show_result)
        self.ui.new_order_btn.clicked.connect(self.addOrder)

    def select(self):
        self.results.clear()
        self.ui.tableWidget.clear()
        # Получение результата запроса
        self.query.exec(f"""select C.name Одежда, M.name Материал, O.quantity Количество,
                        O.amount Стоимость, O.time Время, S.name Статус
                        from Orders O
                        join Cloth C on C.id = O.Cloth_id
                        join Material M on M.id = O.Material_id
                        join Status S on S.id = O.status
                        join User U on U.id = O.User_id where U.login = '{self.login}';""")

        cloth, material, quantity, amount, time, status = range(6)

        while self.query.next():
            self.results.append([self.query.value(cloth), self.query.value(material),
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
        column_headers = ['Одежда', 'Материал', 'Количество', 'Стоимость', 'Время', 'Статус']
        self.ui.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        # Заполнение таблицы
        for row, result in enumerate(self.results):
            for column, value in enumerate(result):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(row, column, item)

        # Изменение размеров строк и столбцов
        self.ui.tableWidget.resizeColumnsToContents()

    def export_table(self):
        wb = openpyxl.Workbook()

        sheet = wb.active

        sheet.append(['Одежда', 'Материал', 'Количество', 'Стоимость', 'Время', 'Статус'])

        # Заполнение таблицы
        for row in self.results:
            sheet.append(row)

        wb.save(f'{self.login}_orders.xlsx')
        wb.close()

        show_message(self, 'Успешно!', 'Файл успешно создан!        ')

    def setupTab(self):
        self.query.exec(f"""select name, id
                            from Cloth;""")

        while self.query.next():
            self.ui.comboBox.addItem(self.query.value(0), self.query.value(1))

        self.query.exec(f"""select name, id
                            from Material;""")

        while self.query.next():
            self.ui.comboBox_2.addItem(self.query.value(0), self.query.value(1))

    def calculate(self):
        self.cloth = self.ui.comboBox.currentText()
        self.material = self.ui.comboBox_2.currentText()
        self.quantity = self.ui.spinBox.value()

        self.query.exec(f"""select req_time, req_material
                            from Cloth
                            where name = '{self.cloth}';""")
        self.query.first()
        self.req_time, self.req_material = float(self.query.value(0)), float(self.query.value(0))

        self.query.exec(f"""select price
                            from Material
                            where name = '{self.material}';""")
        self.query.first()
        self.price = float(self.query.value(0))

        self.amount = self.req_material * self.price * self.quantity
        self.time = self.req_time * self.quantity

    def show_result(self):
        self.calculate()
        font = self.ui.price_label.font()
        font.setBold(True)
        font.setPointSize(14)

        self.ui.price_label.setText(f"Стоимость заказа: {self.amount} руб.")
        self.ui.price_label.setFont(font)

        self.ui.time_label.setText(f"Время ожидания: {self.time} ч.")
        self.ui.time_label.setFont(font)

    def addOrder(self):
        self.calculate()

        self.query.exec(f"""select id from User where login='{self.login}'""")
        self.query.first()
        user_id = int(self.query.value(0))

        self.query.exec(f"""select id from Cloth where name='{self.cloth}'""")
        self.query.first()
        cloth_id = int(self.query.value(0))

        self.query.exec(f"""select id from Material where name='{self.material}'""")
        self.query.first()
        material_id = int(self.query.value(0))

        self.query.exec(f"""insert into Orders (User_id, Cloth_id, Material_id, 
                            quantity, amount, time, status)
                            values 
                            ({user_id}, {cloth_id}, {material_id},
                            {self.quantity}, {self.amount}, {self.time}, 1)""")

        show_message(self, 'Успешно', 'Заказ сделан            ')
