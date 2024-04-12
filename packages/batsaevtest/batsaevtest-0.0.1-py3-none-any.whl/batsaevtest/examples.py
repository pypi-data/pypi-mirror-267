def BD():
    code = """
    # Пример кода для подключения к БД
import pymysql

class Database:
    try:
        def __init__(self, host, user, password, database):
            self.connection = pymysql.connect(host=host, user=user, password=password, database=database)
            self.cursor = self.connection.cursor()
            print(":)")
    except:
        print(":(")

    # Пример запроса в БД
    def get_categ(self):
        query = 'SELECT names FROM types'
        self.cursor.execute(query)
        names = self.cursor.fetchall()
        return [name[0] for name in names]

db = Database(host='localhost', user='root', password='root', database='apteka')
    """
    return code

def main():
    code = """
    # Пример кода для main
import sys
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QLabel,QRadioButton,QCheckBox,QMessageBox,QSpinBox
from PyQt5.uic import loadUi
from database import Database





class Itog(QMainWindow):
    def __init__(self,user_id):
        super(Itog,self).__init__()
        loadUi("itog.ui",self)
        self.user_id = user_id
        self.db = Database(host='localhost', user='root', password='root', database='apteka')
        self.showBasket()
        self.pushButton_3.clicked.connect(self.clear_basket)


    def clear_basket(self):
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)



    def showBasket(self):
        query = f"SELECT nut_id, date, quatity FROM rubbin WHERE user_id = {self.user_id}"
        self.db.cursor.execute(query)
        orders = self.db.cursor.fetchall()

        if orders:
            total_price = 0
            total_items = 0
            order_text = ""
            for order in orders:
                nut_id = order[0]
                query = f"SELECT name, price FROM nutrition WHERE id = {nut_id}"
                self.db.cursor.execute(query)
                result = self.db.cursor.fetchone()
                if result:
                    name, price = result[0], result[1]
                    total_price += price * order[2]
                    total_items += order[2]
                    lb_text = f"РўРѕРІР°СЂ: {name}, Р”Р°С‚Р° Р·Р°РєР°Р·Р°: {order[1]}\n"
                    lb = QLabel(lb_text)
                    order_text = f"РћР±С‰РµРµ РєРѕР»РёС‡РµСЃС‚РІРѕ С‚РѕРІР°СЂРѕРІ: {total_items}\nРћР±С‰Р°СЏ СЃСѓРјРјР°: {total_price}СЂ\n"

                    quatity = int(order[2])
                    spinBox = QSpinBox()
                    spinBox.setValue(quatity)
                    self.formLayout.addWidget(lb)
                    self.formLayout.addWidget(spinBox)

            count_price_text = QLabel(order_text)
            self.verticalLayout.addWidget(count_price_text)






class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super(MainWindow, self).__init__()
        self.user_id = user_id
        loadUi("window.ui", self)
        self.db = Database(host='localhost', user='root', password='root', database='apteka')
        self.comboBox.currentIndexChanged.connect(self.show_tovar)
        self.pushButton.clicked.connect(self.order)
        self.pushButton_2.clicked.connect(self.show_order)
        # self.pushButton_3.clicked.connect(self.back)


        #Combobox
        names = self.db.get_categ()
        self.comboBox.addItems(names)
        #
        # def back(self):
        #     window.destroy()
        #     self.window = Aut()
        #     self.window.show()

        #CheckBox
    def show_tovar(self):
        comboindex = self.comboBox.currentIndex() + 1
        query = f"SELECT id,name,price FROM nutrition WHERE type_id = {comboindex}"
        self.db.cursor.execute(query)
        names = self.db.cursor.fetchall()
        self.db.connection.commit()

        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        for name in names:
            self.box = QCheckBox("{}.{}-{}СЂ".format(name[0],name[1],name[2]))
            self.verticalLayout.addWidget(self.box)

    def order(self):
        if not self.user_id:
            print("РћС€РёР±РєР°: РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ РЅРµ Р°РІС‚РѕСЂРёР·РѕРІР°РЅ.")
            return

        checked_ids = []

        for i in range(self.verticalLayout.count()):
            widget = self.verticalLayout.itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                item_text = widget.text()
                item_id = item_text.split(".")[0]
                checked_ids.append(item_id)

        if checked_ids:
            for item_id in checked_ids:

                query = f"SELECT id FROM rubbin WHERE nut_id = {item_id} AND user_id = {self.user_id}"
                self.db.cursor.execute(query)
                existing_order = self.db.cursor.fetchone()
                if existing_order:

                    update_query = f"UPDATE rubbin SET quatity = quatity + 1 WHERE id = {existing_order[0]}"
                    self.db.cursor.execute(update_query)
                    self.db.connection.commit()
                else:

                    insert_query = f"INSERT INTO rubbin (nut_id, date, quatity, user_id) VALUES ({item_id}, NOW(), 1, {self.user_id})"
                    self.db.cursor.execute(insert_query)
                    self.db.connection.commit()


                    update_query = f"UPDATE nutrition SET quatity = quatity - 1, reserv = reserv + 1 WHERE id = {item_id}"
                    self.db.cursor.execute(update_query)
                    self.db.connection.commit()

            print("Р—Р°РєР°Р· СѓСЃРїРµС€РЅРѕ РґРѕР±Р°РІР»РµРЅ РІ Р±Р°Р·Сѓ РґР°РЅРЅС‹С….")
        else:
            print("РќРµС‚ РѕС‚РјРµС‡РµРЅРЅС‹С… С‚РѕРІР°СЂРѕРІ")

    def show_order(self):
        self.window = Itog(self.user_id)
        self.window.show()

class Aut(QMainWindow):
    def __init__(self):
        super(Aut,self).__init__()
        loadUi("aut.ui",self)
        self.db = Database(host='localhost', user='root', password='root', database='apteka')
        self.pushButton.clicked.connect(self.aut)

    #РђРІС‚РѕСЂРёР·Р°С†РёСЏ
    def aut(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        try:
            query = "SELECT id ,username, password FROM user WHERE username = %s AND password = %s"
            self.db.cursor.execute(query, (login, password))
            result = self.db.cursor.fetchone()

            if result:
                self.user_id = result[0]
                window.hide()
                self.window = MainWindow(self.user_id)
                self.window.show()
            else:
                QMessageBox.critical(self, "РћС€РёР±РєР° РІ Р°РІС‚РѕСЂРёР·Р°С†РёРё",
                                     "РћС€РёР±РєР° РІ Р°РІС‚РѕСЂРёР·Р°С†РёРё\nРќРµРІРµСЂРЅРѕ РЅР°Р±СЂР°РЅ Р»РѕРіРёРЅ РёР»Рё РїР°СЂРѕР»СЊ")
        except Exception as e:
            print("",e)
            QMessageBox.critical(self, "РћС€РёР±РєР°", "РџРѕР»Рµ Р»РѕРіРёРЅ РёР»Рё РїР°СЂРѕР»СЊ РїСѓСЃС‚С‹Рµ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Aut()
    window.show()
    app.exit(app.exec_())
    """
    return code
