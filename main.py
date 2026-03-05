import sys
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from db_connect import db, cursor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cms.ui', self)
        self.id = 0
        self.tb_car.setColumnWidth(0, 50)
        self.tb_car.setColumnWidth(1, 150)
        self.tb_car.setColumnWidth(2, 150)
        self.tb_car.setColumnWidth(3, 150)
        self.tb_car.setColumnWidth(4, 180)

        self.show_all_cars()
        self.btn_add.clicked.connect(self.insert_car) #ทดสอบเวลาปุ่มถูกกด
        self.btn_search.clicked.connect(self.search_car)
        self.tb_car.cellClicked.connect(self.selected_row)

    def selected_row(self):
        row = self.tb_car.currentRow()
        self.id = int(self.tb_car.item(row, 0).text())
        brand = self.tb_car.item(row, 1).text()
        model = self.tb_car.item(row, 2).text()
        year = self.tb_car.item(row, 3).text()
        price = self.tb_car.item(row, 4).text()

        self.txt_brand.setText(brand)
        self.txt_model.setText(model)
        self.txt_year.setText(year)
        self.txt_price.setText(price)


    def say_hi(self):
        QMessageBox.information(self, 'Information', 'Hello World!')
    def search_car(self):
        brand = self.txt_brand.text()
        sql = 'select * from car where brand=?'
        values = (brand,)
        cars = cursor.execute(sql, values).fetchall()
        self.show_all_cars(cars)

        self.txt_search.setText('')


    def show_all_cars(self):
        sql = 'select * from car'
        cars = cursor.execute(sql).fetchall()

        n = len(cars)
        self.tb_car.setRowCount(n)
        row = 0 
        for car in cars:    
            self.tb_car.setItem(row, 0, QTableWidgetItem(str(car[0])))
            self.tb_car.setItem(row, 1, QTableWidgetItem(car[1]))
            self.tb_car.setItem(row, 2, QTableWidgetItem(car[2]))
            self.tb_car.setItem(row, 3, QTableWidgetItem(car[3]))
            self.tb_car.setItem(row, 4, QTableWidgetItem(str(car[4])))
            row += 1



        rs = cursor.execute(sql)
        cars = rs.fetchall()
        self.tb_car.setRowCount(0)
        for row_number, row_data in enumerate(cars):
            self.tb_car.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tb_car.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    def insert_car(self):
        brand = self.txt_brand.text()
        model = self.txt_model.text()
        year = self.txt_year.text()
        price = self.txt_price.text()
        sql = 'insert into car(brand, model, year, price) values(?, ?, ?, ?);'
        values = (brand, model, year, price)

        rs = cursor.execute(sql, values)
        db.commit()
        if rs.rowcount>0:
            QMessageBox.information(self, 'Information', 'insert car successful!')
            self.senddis(f"รถ {brand}\n{model}\nปี {year}\nราคา {price}")
        else:
            QMessageBox.warning(self, 'warning', 'Unable to insert car!')
        
        self.clear()
    def clear(self):
        self.txt_brand.setText('')
        self.txt_model.setText('')
        self.txt_year.setText('')
        self.txt_price.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
