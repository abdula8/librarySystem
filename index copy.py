from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import MySQLdb
import datetime
from datetime import date
import sys
from os import system
from os import chdir
import re
from xlsxwriter import *
from xlrd import *
import hashlib
import pyqtgraph as pg

# system('cls')
# path = ''
# chdir()

MainUI, _ = loadUiType('main.ui')

employee_id = 0
employee_branch = 0



class Main(QMainWindow, MainUI):
    # enter_pressed = pyqtSignal()
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Db_Connect()
        self.Handle_Buttons()
        self.UI_Changes()
        self.get_dashboard_data()

        self.Open_Login_Tab()
        #self.Open_Daily_movements_Tab()
        self.Show_All_Categories()
        self.Show_Branches()
        self.Show_publisher()
        self.Show_Authors()
        self.Show_All_Books()
        self.Show_All_Clients()
        self.Retreive_Day_Work()
        self.Show_Employee()
        self.Show_History()

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Return:
    #         self.enter_pressed.emit()
    #         self.User_Login_permissions
    #         print("Enter key is pressed!!!!!")
    #     else:
    #         QComboBox.keyPressEvent(self, event)
            # if the key is not return, handle normally
    def PopUpMessage(self, message, title):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        # msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def UI_Changes(self):
        ## UI_Changes in login
        # the code to hide the tab bar
        self.tabWidget.tabBar().setVisible(False)

    def Db_Connect(self):
        ## Connection between app and DB
        self.db = MySQLdb.connect(host='localhost', user='root', password='01099110790aA@', db='library')
        print('Connection Accepted')
        # we need to create a cursor that make the transfer method between human and database that
        # you send file query and it returns data
        self.cur = self.db.cursor()



    def Handle_Buttons(self):
        ## Habdle All Buttons
        self.pushButton.clicked.connect(self.Open_Daily_movements_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_4.clicked.connect(self.Open_Dahsboard_Tab)
        self.pushButton_6.clicked.connect(self.Open_History_Tab)
        self.pushButton_7.clicked.connect(self.Open_Reports_Tab)
        self.pushButton_5.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_20.clicked.connect(self.Add_Branch)
        self.pushButton_21.clicked.connect(self.Add_Puplisher)
        self.pushButton_22.clicked.connect(self.Add_Auther)
        self.pushButton_23.clicked.connect(self.Add_Category)
        self.pushButton_26.clicked.connect(self.Add_Employee)

        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_14.clicked.connect(self.Edit_Book_search)
        self.pushButton_13.clicked.connect(self.Edit_Book)
        self.pushButton_15.clicked.connect(self.Delete_Book)
        self.pushButton_9.clicked.connect(self.All_Book_Filter)
        self.pushButton_35.clicked.connect(self.Books_Export_Report)

        self.pushButton_17.clicked.connect(self.Add_New_Client)
        self.pushButton_19.clicked.connect(self.Edit_Client_Search)
        self.pushButton_18.clicked.connect(self.Edit_Client)
        self.pushButton_27.clicked.connect(self.Delete_Client)
        self.pushButton_37.clicked.connect(self.Client_Export_Report)

        # self.pushButton_5.clicked.connect(self.Handle_to_Day_Work)
        self.pushButton_8.clicked.connect(self.Handle_to_Day_Work)

        self.pushButton_29.clicked.connect(self.Check_Employee)
        self.pushButton_28.clicked.connect(self.Edit_Employee_Data)
        self.pushButton_30.clicked.connect(self.Add_Employee_Permissions)
        # self.pushButton_31.clicked.connect(self.Check_Employee_Permissions)
        self.checkBox_23.clicked.connect(self.Check_Employee_Permissions)

        self.pushButton_38.clicked.connect(self.User_Login_permissions)
        # self.pushButton_38.clicked.connect(self.User_Logout)
        self.pushButton_48.clicked.connect(self.Show_Password)

        self.pushButton_42.clicked.connect(self.get_dashboard_data)


    def Handle_Login(self):
        ## HAndle Login
        pass
    def Handle_Reset_Passwords(self):
        ## Handle  Reset Password
        pass
    def history(self, action=2, table=0, general_value=None):
                global employee_id, employee_branch
                self.cur.execute('''
                    INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch, data)
                    VALUES(%s,%s,%s,%s,%s,%s)
                ''',(employee_id, action, table, date, employee_branch, general_value))

                self.Show_History()
    def Handle_to_Day_Work(self):
        ## Handle todat Work
        book_title = self.lineEdit_12.text()
        client_national_id = self.lineEdit_42.text()
        type_of = self.comboBox.currentIndex()
        from_date = datetime.date.today()
        # to_date = str(datetime.date.today())
        to_date_py = self.dateEdit_7.date().toPyDate()
        print("from date: ", type(from_date), "To date: ", type(to_date_py))
        if to_date_py < from_date:
            self.PopUpMessage("It's a past date not future ", "Congratulations")

        else:
            to_date = str(to_date_py)
            date = datetime.datetime.now()
            branch = 1
            employee = 1

            self.cur.execute('''
                    INSERT INTO daily_movement(book_id, client_id, type_of, date, branch_id, Book_from, Book_to, employee_id)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',(book_title, client_national_id, type_of, date, branch, from_date, to_date, employee))

            ## History
            self.history(action=2, table=0, data = "Day to Day Work")
        ## history above

        self.db.commit()
        # print("DONE....!!!")
        self.Retreive_Day_Work()


    def Retreive_Day_Work(self):
        self.cur.execute('''
            SELECT book_id, type_of, client_id, Book_from, Book_to FROM daily_movement
        ''')
        data = self.cur.fetchall()
        # print(data)
        '''compare date from database to date of now'''
        self.cur.execute('''SELECT date FROM daily_movement''')
        one_date = self.cur.fetchone()
        if one_date:
            # print("\n\n\n\n\n\n", "Date from DataBase = ", one_date[0], "Type is: ", type(one_date[0]), "\n\n\n\n\n\n")
            date_check = datetime.datetime.now() - one_date[0]
            # print("\n\n\n\n\n\n", "date_check", date_check, "\n", "date_check.days = ", date_check.days, "Type: ", type(date_check), "\n\n\n\n\n\n")

            if date_check.days == 0:
                # print("\n\n\n\n\n\n", "000000000000 = ", date_check.days, "Type: ", type(date_check),
                #       "\n\n\n\n\n\n")
                self.tableWidget.setRowCount(0)
                self.tableWidget.insertRow(0)
                for row, form in enumerate(data):
                    for column, item in enumerate(form):
                        if column == 1:
                            if item == 0:
                                self.tableWidget.setItem(row, column, QTableWidgetItem("Rent"))
                            else:
                                self.tableWidget.setItem(row, column, QTableWidgetItem("Retrieve"))
                        elif column == 2:
                            sql = '''SELECT name FROM clients WHERE national_id=%s'''
                            self.cur.execute(sql, [(item)])
                            client_name = self.cur.fetchone()
                            # print(client_name)
                            if client_name:
                                self.tableWidget.setItem(row, column, QTableWidgetItem(str(client_name[0])))
                            else:
                                self.tableWidget.setItem(row, column, QTableWidgetItem(str(client_name)))
                        else:
                            self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

                        column += 1
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
            else:
                self.cur.execute('''
                            SELECT book_id, client_id, type_of, date, branch_id, Book_to, employee_id FROM daily_movement
                        ''')
                data = self.cur.fetchall()
                excel_file = Workbook('daily_movements_report.xlsx')
                sheet1 = excel_file.add_worksheet()
                sheet1.write(0, 0, 'Book ID')
                sheet1.write(0, 1, 'Client ID')
                sheet1.write(0, 2, 'Type')
                sheet1.write(0, 3, 'Date')
                sheet1.write(0, 4, 'Branch ID')
                sheet1.write(0, 5, 'Book from')
                sheet1.write(0, 6, 'Book to')
                sheet1.write(0, 7, 'Employee ID')

                row_number = 1
                for row in data:
                    column_number = 0
                    for item in row:
                        sheet1.write(row_number, column_number, str(item))
                        column_number += 1
                    row_number += 1
                excel_file.close()

                sql = ('''DELETE FROM daily_movement''')
                self.cur.execute(sql, )
                self.db.commit()

    #############################################################
    #############################################################
    def Show_All_Books(self):
        ## show all books
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        self.cur.execute('''
            SELECT code, title, category_id, auther_id, price FROM books
            ''')
        data = self.cur.fetchall()
        # print(data[0][4])

        self.cur.execute('''SELECT id FROM category''')
        categories = self.cur.fetchall()
        categories = sorted(categories)

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 2:
                    sql = '''SELECT category FROM category WHERE id=%s'''
                    # print("\n\n\n", type(item), "\n\n\n", form,"\n\n\n", "\n\n\n", len(form),"\n\n\n", "\n\n\n", form[item-2],"\n\n\n" )
                    # if item == 0:
                    #     self.cur.execute(sql, [(5)])
                    # else:
                    self.cur.execute(sql, [(categories[item])])
                    category_name = self.cur.fetchone()
                    # print(category_name)
# to add a value in the following line it must be with type "QTableWidgetItem" nad it takes string argument
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))
                elif col == 3:
                    sql = '''SELECT name FROM auther WHERE id=%s'''
                    self.cur.execute(sql, [(item+1)])
                    author_name = self.cur.fetchone()
                    # print(author_name)

                    # self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)


    def Add_New_Book(self):
        ## add new book
        book_title = self.lineEdit_2.text()
        description = self.textEdit.toPlainText()
        category = self.comboBox_3.currentIndex()
        price = self.lineEdit_3.text()
        code = self.lineEdit_4.text()
        publisher = self.comboBox_4.currentIndex()
        author = self.comboBox_5.currentIndex()
        status = self.comboBox_6.currentIndex()
        part_order = self.lineEdit_36.text()
        barcode = self.lineEdit_40.text()
        date = datetime.datetime.now()

        self.cur.execute('''
            INSERT INTO books(title,description,category_id,code,barcode,part_order,price,publisher_id,auther_id,status,date)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (book_title, description, category, code, barcode, part_order, price,  publisher, author, status, date))

        ## History
        self.history(book_title)
        
        self.db.commit()
        self.PopUpMessage("تم إضافة الكتاب الى قاعدة البيانات.", "عملية صحيحة")
        self.lineEdit_2.setText('')
        self.textEdit.setText('')
        # self.comboBox_3.currentIndex()
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        # self.comboBox_4.currentIndex()
        # self.comboBox_5.currentIndex()
        # self.comboBox_6.currentIndex()
        self.lineEdit_36.setText('')
        self.lineEdit_40.setText('')

        self.Show_All_Books()

    def All_Book_Filter(self):
        book_title = self.lineEdit.text()
        category = self.comboBox_2.currentIndex()
        # all_categories = self.comboBox_2.allItems()
        # number_of_categories = len(all_categories)

        sql = ''' SELECT code, title, category_id, publisher_id, auther_id FROM books WHERE title=%s AND category_id=%s'''
        self.cur.execute(sql, [book_title, category])
        data = self.cur.fetchall()
        # print("\n\n", type(data), "\n\n")
        # self.statusBar().showMessage("تم تعديل معلومات الكتاب بنجاح")
        # self.PopUpMessage("تم تعديل معلومات الكتاب بنجاح", "Congratulations")
        # QMessageBox.information(self, "Success", "تم تعديل معلومات الكتاب بنجاح")
        print("Done")
        # self.lineEdit.text()
        # self.comboBox_2.currentIndex()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
               if col == 2:
                   sql = '''SELECT category FROM category WHERE id=%s'''
                   # print("\n\n\n", type(item), "\n\n\n", type(form),"\n\n\n" )
                   self.cur.execute(sql, [(item)])
                   category_name = self.cur.fetchone()
                   print("category_name: ", category_name)

                   self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                   # self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name)))
               else:
                   # self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name)))
                   self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                   print(item)
               col += 1
            # print(item)
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)

    def Edit_Book(self):
        book_title = self.lineEdit_11.text()
        description = self.textEdit_3.toPlainText()
        category = self.comboBox_13.currentIndex()
        price = self.lineEdit_10.text()
        code = self.lineEdit_9.text()
        publisher = self.comboBox_15.currentIndex()
        author = self.comboBox_12.currentIndex()
        status = self.comboBox_14.currentIndex()
        part_order = self.lineEdit_41.text()
        date = datetime.datetime.now()
        # price = price[:-3]
        exceptVar = 0

        try:
            self.cur.execute('''
                        UPDATE books SET title=%s, description=%s, category_id=%s, code=%s, part_order=%s, price=%s, publisher_id=%s, auther_id=%s, status=%s WHERE code=%s
                ''', (book_title, description, category, code, part_order, price, publisher, author, status, code))
        except Exception as e:
            exceptVar = 1
            # self.PopUpMessage(str(e[1]), "Error")
            # print(str(e[1]))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()

        ## History
        global employee_id, employee_branch
        action = 3
        table = 0
        self.cur.execute('''
            INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch, data)
            VALUES(%s,%s,%s,%s,%s,%s)
                ''', (employee_id, action, table, date, employee_branch,book_title))
        self.Show_History()
        ## history above

        self.db.commit()
        if not exceptVar:
            self.statusBar().showMessage("تم تعديل معلومات الكتاب بنجاح")
            self.PopUpMessage("تم تغديل الكتاب", "DONE")
        # self.PopUpMessage("تم تعديل معلومات الكتاب بنجاح", "Congratulations")
        # QMessageBox.information(self, "Success", "تم تعديل معلومات الكتاب بنجاح")
        print("Done")

        self.Show_All_Books()


    def Edit_Book_search(self):
        ## edit book
        book_code = self.lineEdit_9.text()
        sql = ('''
            SELECT * FROM books WHERE code = %s
            ''')
        self.cur.execute(sql, [(book_code)])
        data = self.cur.fetchone()
        # print(data)

        self.lineEdit_11.setText(data[1]) # Book Title
        self.comboBox_13.setCurrentIndex(data[12]) # Category
        self.lineEdit_10.setText(str(data[6])[:-3]) # Price   we used [:-3] to display only 2 deciml numbers after point ==> 21-4-2022_0303AM
        self.comboBox_15.setCurrentIndex(data[10]) # Publisher
        self.comboBox_12.setCurrentIndex(data[11]) # Author
        self.comboBox_14.setCurrentIndex(int(data[8])) # status
        # print(int(data[8]))
        self.lineEdit_41.setText(str(data[5])) # Part Order
        self.textEdit_3.setPlainText(data[2])


    def Delete_Book(self):
        ## delete book from DB
        book_code = self.lineEdit_9.text()
        delete_message = QMessageBox.warning(self, "Delete info.", "هل انت متأكد من انك تريد مسح الكتاب؟", QMessageBox.Yes| QMessageBox.No)
        if delete_message==QMessageBox.Yes:
            sql =('''DELETE FROM books WHERE code=%s''')
            self.cur.execute(sql, [(book_code)])
            self.statusBar().showMessage("تم مسح الكتاب بنجاح")
            self.PopUpMessage("تم مسح الكتاب بنجاح", "مبروك")

            ## History
            date = datetime.datetime.now()
            global employee_id, employee_branch
            action = 4
            table = 0
            self.cur.execute('''
                INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
                VALUES(%s,%s,%s,%s,%s,%s)
            ''', (employee_id, action, table, date, employee_branch,book_code))
            self.Show_History()
            self.db.commit()
            ## history above
            # self.PopUpMessage("تم مسح الكتاب", "DONE")

            self.Show_All_Books()
        else:
            self.statusBar().showMessage("لم يتم مسح الكتاب")


    ###################################################################3
    def Show_All_Clients(self):
        ## show all Clients
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)

        self.cur.execute('''
            SELECT name, mail, phone, national_id, date FROM clients
            ''')
        data = self.cur.fetchall()
        # print(data)

        ## row = iteration, form = data
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)


    def Add_New_Client(self):
        ## add new Client
        client_name         = self.lineEdit_14.text()
        client_email        = self.lineEdit_15.text()
        client_phone        = self.lineEdit_16.text()
        client_national_id  = self.lineEdit_17.text()

        date = datetime.datetime.now()

        mail_pattern = re.match(r'^[a-zA-Z][\w\-.]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$', client_email)
        phon_pattern = re.match(r'^01[\d]{9}$', str(client_phone))
        naID_pattern = re.match(r'^[\d]{14}$', str(client_national_id))
        if mail_pattern and phon_pattern and naID_pattern:
            self.cur.execute('''
                INSERT INTO clients(name, mail, phone, national_id, date)
                VALUES (%s,%s,%s,%s,%s)
                ''', (client_name, client_email, client_phone, client_national_id, date))

            ## History
            date = datetime.datetime.now()
            global employee_id, employee_branch
            action = 2
            table = 1
            self.cur.execute('''
                INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
                VALUES(%s,%s,%s,%s,%s,%s)
            ''', (employee_id, action, table, date, employee_branch,client_name))
            self.Show_History()
            ## history above

            self.db.commit()
            self.PopUpMessage("تم إضافة العميل", "DONE")
            self.lineEdit_14.setText('')
            self.lineEdit_15.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit_17.setText('')
            self.Show_All_Clients()
            print("Done")
        else:
            self.PopUpMessage("Enter email in correct format:\n \"example.er.9@example.com\"", "Incorrect")

    def Edit_Client_Search(self):
        ## edit Client
        client_data = self.lineEdit_22.text()

        if self.comboBox_16.currentIndex() == 0:
            sql = ('''SELECT * FROM clients WHERE mail = %s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()
            # print(data)

        elif self.comboBox_16.currentIndex() == 1:
            sql = ('''SELECT * FROM clients WHERE national_id = %s''')
            self.cur.execute(sql, [(client_data)])
            data = self.cur.fetchone()
            # print(data)

        self.lineEdit_20.setText(data[1]) # name
        self.lineEdit_21.setText(data[2]) # mail
        self.lineEdit_18.setText(data[3]) # phone
        self.lineEdit_19.setText(str(data[5])) # national id

        ######### You can do that which you will search without need
        ######### for the combo box that contains (name, id, phone, and name)
        # sql = ('''
        #             SELECT * FROM clients WHERE name = %s OR mail = %s OR national_id=%s OR phone=%s
        #             ''')
        #
        # self.cur.execute(sql, [(client_data), (client_data), (client_data), (client_data)])
        ## data = self.cur.fetchone()
        ## print(data)
        ##



    def Edit_Client(self):
        # edit client
        client_name = self.lineEdit_20.text() # name
        client_mail = self.lineEdit_21.text() # mail
        client_phone = self.lineEdit_18.text() # phone
        client_national_id = self.lineEdit_19.text() # national id

        # self.cur.execute('''UPDATE clients SET name=%s, mail=%s, phone=%s, national_id=%s
        #                 ''', (client_name, client_mail, client_phone, client_national_id))

        self.cur.execute('''
                    UPDATE clients SET name=%s, mail=%s, phone=%s, national_id=%s WHERE name = %s OR mail = %s OR national_id=%s OR phone=%s
                ''', (client_name, client_mail, client_phone, client_national_id, client_name, client_mail, client_phone, client_national_id))

        ## History
        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 3
        table = 1
        self.cur.execute('''
            INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
            VALUES(%s,%s,%s,%s,%s,%s)
        ''', (employee_id, action, table, date, employee_branch,client_name))
        self.Show_History()
        ## history above

        self.db.commit()
        self.statusBar().showMessage("تم تعديل معلومات العميل بنجاح")
        self.PopUpMessage("تم تعديل العميل", "DONE")
        ## to clear text from text boxes after ending the editng
        self.lineEdit_20.setText('')  # name
        self.lineEdit_22.setText('')  # name
        self.lineEdit_21.setText('')  # mail
        self.lineEdit_18.setText('')  # phone
        self.lineEdit_19.setText('')  # national id
        self.Show_All_Clients()

        # self.PopUpMessage("تم تعديل معلومات الكتاب بنجاح", "Congratulations")
        # QMessageBox.information(self, "Success", "تم تعديل معلومات الكتاب بنجاح")

    def Delete_Client(self):
        ## delete Client from DB
        client_data = self.lineEdit_22.text()

        delete_message = QMessageBox.warning(self, "Delete info.", "هل انت متأكد من انك تريد مسح العميل؟", QMessageBox.Yes| QMessageBox.No)
        if delete_message == QMessageBox.Yes:

            if self.comboBox_16.currentIndex() == 0:
                sql = ('''DELETE FROM clients WHERE mail = %s ''')
                self.cur.execute(sql, [(client_data)])
                data = self.cur.fetchone()
                # print(data)

            elif self.comboBox_16.currentIndex() == 1:
                sql = ('''DELETE FROM clients WHERE national_id = %s ''')
                self.cur.execute(sql, [(client_data)])
                data = self.cur.fetchone()
                # print(data)

            ## History
            date = datetime.datetime.now()
            global employee_id, employee_branch
            action = 4
            table = 1
            self.cur.execute('''
                    INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
                    VALUES(%s,%s,%s,%s,%s,%s)
                ''', (employee_id, action, table, date, employee_branch,client_data))
            self.Show_History()
            ## history above

            self.db.commit()
            self.statusBar().showMessage("تم مسح بيانات العميل بنجاح")
            self.PopUpMessage("تم مسح العميل", "DONE")
            ## to clear text from text boxes after ending the editng
            self.lineEdit_20.setText('')  # name
            self.lineEdit_22.setText('')  # name
            self.lineEdit_21.setText('')  # mail
            self.lineEdit_18.setText('')  # phone
            self.lineEdit_19.setText('')  # national id
            print(":Done:::!!!")

            self.Show_All_Clients()


    ####################################################################
    ## history

    def Show_History(self):
        ## show all history to the admin
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)

        self.cur.execute('''
           SELECT employee_id, employee_branch_id, employee_action, effected_table, operation_date, data FROM history
           ''')

        data = self.cur.fetchall()
        # print(data)

        ## row = iteration, form = data
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                # print(row)
                if col == 0:
                    sql = '''SELECT name FROM employee WHERE id=%s'''
                    self.cur.execute(sql, [(item)])
                    employee_name = self.cur.fetchone()
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(employee_name)))

                elif col == 1:
                    # print("\n\n\n\n", "Branch ID = %s"%item, "\n\n\n\n")
                    sql = '''SELECT name FROM branch WHERE id=%s'''
                    self.cur.execute(sql, [(item+1)])
                    branch_name = self.cur.fetchone()
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(branch_name)))

                elif col == 2:
                    action = " "
                    if item == 0:
                        action = "Login"
                    elif item == 1:
                        action = "Logout"
                    elif item == 2:
                        action = "Add"
                    elif item == 3:
                        action = "Edit"
                    elif item == 4:
                        action = "Delete"
                    elif item == 5:
                        action = "Search"
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(action)))

                elif col == 3:
                    table = " "
                    if item == 0:
                        table = "Books"
                    elif item == 1:
                        table = "Clients"
                    elif item == 2:
                        table = "History"
                    elif item == 3:
                        table = "Branch"
                    elif item == 4:
                        table = "Category"
                    elif item == 5:
                        table = "Daily Movements"
                    elif item == 6:
                        table = "Employee"
                    elif item == 7:
                        table = "Publisher"
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(table)))

                elif col == 4:
                    sql = '''SELECT operation_date FROM history WHERE operation_date=%s'''
                    # print("\n\n\n\n\n\n", "item = ", item, "\n\n\n\n\n\n\n")
                    self.cur.execute(sql, [(item)])

                    date = self.cur.fetchone()
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(date[0])))

                elif col == 5:
                    # print(data[5],"\n\n")
                    # print("item",item,"\n\n")
                    sql = '''SELECT data FROM history WHERE data=%s'''
                    self.cur.execute(sql, [(item)])
                    extra_data = self.cur.fetchone()
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(extra_data[0])))

            col += 1
            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)


    ####################################################################
    ## books report
    def All_Books_report(self):
        ## report for all books
        pass
    def Books_Filter_Report(self):
        ## Show Report For Filtered Books
        pass
    def Books_Export_Report(self):
        ## Export Books Data To Export File
        self.cur.execute('''
            SELECT code, title, category_id, auther_id, price FROM books
            ''')
        data = self.cur.fetchall()
        excel_file = Workbook('books_report.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0,0, 'Book Code')
        sheet1.write(0,1, 'Book Title')
        sheet1.write(0,2, 'Category')
        sheet1.write(0,3, 'Author')
        sheet1.write(0,4, 'Price')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number,column_number, str(item))
                column_number += 1
            row_number += 1
        excel_file.close()
        print("Exported Correctly...")
        self.statusBar().showMessage("تم إضافة الموظف بنجاح")

    ####################################################################
    ## books report
    def All_Clients_report(self):
        ## report for all Clients
        pass
    def Clients_Filter_Report(self):
        ## Show Report For Filtered Clients
        pass
    def Client_Export_Report(self):
        ## Export Client Data To Ecel File

        self.cur.execute('''
            SELECT name, mail, phone, national_id FROM clients
            ''')
        data = self.cur.fetchall()

        excel_file = Workbook('clients_report.xlsx')
        sheet1 = excel_file.add_worksheet()
        sheet1.write(0, 0, 'Client Name')
        sheet1.write(0, 1, 'Client MAil')
        sheet1.write(0, 2, 'Client Phone')
        sheet1.write(0, 3, 'Client National ID')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1
        excel_file.close()
        print("Exported Correctly...")
        self.statusBar().showMessage("تم إضافة الموظف بنجاح")

    ####################################################################
    ## books report

    def Monthly_Report(self):
        ## Show one month report
        pass
    def Monthly_Report_Export(self):
        ## export monthly report
        pass
    ####################################################################
    ####################################################################
    ## settings
    def Add_Branch(self):
        ## add new  branch
        branch_name = self.lineEdit_23.text()
        branch_code = self.lineEdit_24.text()
        branch_location = self.lineEdit_25.text()

        self.cur.execute('''
            INSERT INTO branch (name, code, location)
            VALUES(%s, %s, %s)
        ''', (branch_name, branch_code, branch_location)
        )

        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 2
        table = 2
        ## the following line contains errors in names of tables or columns ==>
        # ==> employee_action = action
        # ==> effected_table  = table
        # ==> operation_date  = date
        # ==> employee_branch = branch
        # ==>                 = data       this column is not in the table till that is created using code(DB_Structure.py)
        try:
            self.cur.execute('''
               INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch_id,data)
               VALUES(%s,%s,%s,%s,%s,%s)
           ''', (employee_id, action, table, date, employee_branch,branch_name))
        except:
            pass
        self.Show_History()
        self.db.commit()
        print('Branch Added')

    def Add_Category(self):
        ## add new category
        category_name = self.lineEdit_30.text()
        parent_category_text = self.comboBox_7.currentText()
        print(parent_category_text, type(parent_category_text))

        query = '''SELECT id FROM category WHERE category = %s'''
        self.cur.execute(query, [(parent_category_text)])
        data = self.cur.fetchone()
        #print(data, type(data), len(data), "Data: ", data[0], type(data[0]))
        parent_category = data[0]

        self.cur.execute(
            '''
            INSERT INTO category (category, parent_category)
            VALUES(%s, %s)
            ''', (category_name, parent_category)
        )

        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 2
        table = 3
        self.cur.execute('''
               INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
               VALUES(%s,%s,%s,%s,%s,%s)
           ''', (employee_id, action, table, date, employee_branch, category_name))
        self.Show_History()

        self.db.commit()
        print('Category Added')
        self.lineEdit_30.setText('')
        self.Show_All_Categories()

    def  Add_Puplisher(self):
        ## add new puplisher

        publisher_name = self.lineEdit_26.text()
        publisher_location = self.lineEdit_28.text()

        self.cur.execute(
            '''
            INSERT INTO publisher (name, location)
            VALUES(%s, %s)
            ''', (publisher_name, publisher_location)
        )

        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 2
        table = 7
        self.cur.execute('''
               INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
               VALUES(%s,%s,%s,%s,%s,%s)
           ''', (employee_id, action, table, date, employee_branch, publisher_name))
        self.Show_History()

        self.db.commit() # to save data on hard disk not only ram
        print('Publisher Added')
        self.lineEdit_26.text('')
        self.lineEdit_28.text('')

    def Add_Auther(self):
        ## add new auther

        author_name = self.lineEdit_29.text()
        author_location = self.lineEdit_31.text()

        self.cur.execute(
            '''
            INSERT INTO auther (name, location)
            VALUES(%s, %s)
            ''', (author_name, author_location)
        )

        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 2
        table = 8
        self.cur.execute('''
               INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
               VALUES(%s,%s,%s,%s,%s,%s)
           ''', (employee_id, action, table, date, employee_branch,author_name))
        self.Show_History()

        self.db.commit() # to save data on hard disk not only ram
        print('Author Added')
        self.lineEdit_29.text('')
        self.lineEdit_31.text('')
        self.Show_Authors()

    #############################################################
    #############################################################


    def Show_Branches(self):

        self.cur.execute('''
            SELECT name FROM branch
        ''')

        branches = self.cur.fetchall()
        for branch in branches:
            self.comboBox_21.addItem(branch[0])
            self.comboBox_22.addItem(branch[0])

    def Show_publisher(self):
        self.cur.execute('''
                    SELECT name FROM publisher
                ''')
        publishers = self.cur.fetchall()
        for publisher in publishers:
            self.comboBox_15.addItem(publisher[0])
            self.comboBox_4.addItem(publisher[0])

    def Show_Authors(self):

        """
        We want to get the correct Author ID to to get correct name from DataBase
        to do that...
            - from "authors" previous tuple we can get the correct id we that we want
            - firstly: we create a for loop to loop on tuple
            - then

        """

        self.cur.execute('''SELECT id FROM auther''')
        authors = self.cur.fetchall()
        authors = sorted(authors)
        # print("\n\n\n", "Show Authors Function", "\n\n\n", authors, "\n\n\n", "Authors Printed Correctly","\n\n\n\n")
        for author in authors:
            ''' select by current index the text( book author ) '''
            self.cur.execute('''SELECT name FROM auther WHERE id=%s''', (author))
            author_name = self.cur.fetchone()
            # self.comboBox_12.addItem(str(author[0]))
            self.comboBox_12.addItem(str(author_name[0]))
            self.comboBox_5.addItem(str(author_name[0]))



    def Show_All_Categories(self):
        self.comboBox_7.clear()
        self.comboBox_3.clear()
        self.comboBox_13.clear()
        self.comboBox_2.clear()
        # Get category name
        self.cur.execute('''SELECT id FROM category''')
        categories = self.cur.fetchall()
        categories = sorted(categories)
        # print("categories", categories)
        for category in categories:
            self.cur.execute('''SELECT category FROM category WHERE id=%s''', (category,))
            category_name = self.cur.fetchone()
            # print("Category", category)
            self.comboBox_7.addItem(str(category_name[0]))
            self.comboBox_3.addItem(str(category_name[0]))
            self.comboBox_13.addItem(str(category_name[0]))
            self.comboBox_2.addItem(str(category_name[0]))



    ####################################################################
    ####################################################################
    ## Employee
    def Add_Employee(self):
        ## add new employee
        employee_name       = self.lineEdit_33.text()
        employee_mail       = self.lineEdit_27.text()
        employee_phone      = self.lineEdit_32.text()
        employee_branch_    = self.comboBox_21.currentIndex()
        national_id         = self.lineEdit_34.text()
        priority            = self.lineEdit_35.text()
        password            = self.lineEdit_37.text()
        password_2          = self.lineEdit_52.text()

        date = datetime.datetime.now()
        # date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 2
        table = 6
        # print(date)
        '''
        
        password encryption:
            query ==>> SELECT password FROM employee WHERE encrypted_password=%s,(encrypted)
            it may be not fetching data in plaintext you may ==> fetch encryption keys itself
            
            1- generate_key
            2- save_key in text file
            3- encrypt password 
            4- save encrypted_password in database
            ** then to check the passwords:
            1- fetch encrypted_password from database
            2- decrypt password by key saved in text file before
            3- Check encryption to each others not passwords themselves
             
        '''
        if password == password_2:
            self.cur.execute('''
                INSERT INTO employee (name, mail, phone, date, national_id, priority, password, branch)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                ''', (employee_name, employee_mail, employee_phone, date, national_id, priority, password, employee_branch))
            ## History
            try:
                self.cur.execute('''
                    INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch_id,data)
                    VALUES(%s, %s, %s, %s, %s, %s)
                ''', (employee_id, action, table, date, employee_branch_,employee_name))
            except:
                pass
            self.Show_History()
            ## history above

            self.db.commit()
            self.lineEdit_33.setText('')
            self.lineEdit_27.setText('')
            self.lineEdit_32.setText('')
            self.lineEdit_34.setText('')
            self.lineEdit_35.setText('')
            self.lineEdit_37.setText('')
            self.lineEdit_52.setText('')
            self.statusBar().showMessage("تم إضافة الموظف بنجاح")
            self.PopUpMessage("تم إضافة الموظف بنجاح", "Password Correct")
            # import winsound
            # duration = 1000  # milliseconds
            # freq = 440  # Hz
            # winsound.Beep(freq, duration)
        else:
            print("Wrong Password!!")
            self.PopUpMessage("Your passwords don't matches please enter the second one again>>>", "Password Error")
            self.lineEdit_37.setText('')#password
            self.lineEdit_52.setText('')#password_2

    def Check_Employee(self):
        employee_mail = self.lineEdit_47.text()
        employee_password = self.lineEdit_48.text()

        sql = '''SELECT * from employee'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        # print(data)

        for row in data:
            if row[2] == employee_mail and row[7] == employee_password:
                # print(row)
                self.groupBox_9.setEnabled(True)
                self.lineEdit_45.setText(row[1]) ## name
                self.lineEdit_49.setText(row[3]) ## phone
                self.comboBox_22.setCurrentIndex(row[8]) ## branch
                self.lineEdit_50.setText(row[5]) ## National ID
                self.lineEdit_51.setText(row[6]) ## Priority
                self.lineEdit_46.setText(row[7]) ## Password
            # else:
            #     QMessageBox.information(self, "Success", "User name or password incorrect try again")
            #     continue

    def Edit_Employee_Data(self):
        ## edit employee data
        employee_name = self.lineEdit_47.text()
        employee_password = self.lineEdit_48.text()

        # employee_mail = self.lineEdit_45.text()
        employee_phone = self.lineEdit_49.text()
        date = datetime.datetime.now()
        national_id = self.lineEdit_50.text()
        priority = self.lineEdit_51.text()
        password = self.lineEdit_46.text()
        employee_branch_ = self.comboBox_22.currentIndex()
        # employee_branch = "Alex"
        # date = datetime.datetime.now()

        global employee_id, employee_branch
        action = 3
        table = 6

        if employee_password == password:
            self.cur.execute('''
                    UPDATE employee SET name =%s,phone=%s,priority=%s,password=%s,branch=%s  WHERE national_id = %s
            ''',(employee_name, employee_phone, priority, password, employee_branch_, national_id))

        self.cur.execute('''
                INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
                VALUES(%s,%s,%s,%s,%s,%s)
            ''', (employee_id, action, table, date, employee_branch,employee_name))
        self.Show_History()

        self.db.commit()

        self.lineEdit_47.setText('')
        self.lineEdit_48.setText('')
        #self.lineEdit_45.setText('')
        self.lineEdit_49.setText('')
        self.lineEdit_50.setText('')
        self.lineEdit_51.setText('')
        self.lineEdit_46.setText('')
        self.comboBox_22.setCurrentIndex(0)
        self.groupBox_9.setEnabled(False)
        print("Done")

    def Show_Employee(self):
        self.cur.execute('''SELECT mail FROM employee''')
        employees = self.cur.fetchall()
        for employee in employees:
            self.comboBox_18.addItem(employee[0])
            self.comboBox_10.addItem(employee[0])
    ####################################################################
    ####################################################################
    ## Employee


    def Check_Employee_Permissions(self):
    #     employee_name = self.comboBox_18.currentText()
    #     self.cur.execute('''
    #             SELECT employee_name FROM employee_permissions WHERE 1=1
    #     ''')
    #     names = self.cur.fetchall()
    #     if employee_name in names:
    #         pass
        if not (self.checkBox_23.isChecked()):
            self.groupBox_10.setEnabled(True)
            self.groupBox_11.setEnabled(True)
            self.groupBox_12.setEnabled(True)
            self.groupBox_13.setEnabled(True)
        else:
            self.groupBox_10.setEnabled(False)
            self.groupBox_11.setEnabled(False)
            self.groupBox_12.setEnabled(False)
            self.groupBox_13.setEnabled(False)


    def Add_Employee_Permissions(self):
        ##  add permissions to any employee

        employee_name = self.comboBox_18.currentText()
        is_admin = 0

        books_tab = 0
        clients_tab = 0
        dashboard_tab = 0
        history_tab = 0
        reports_tab = 0
        settings_tab = 0

        add_book = 0
        edit_book = 0
        delete_book = 0
        import_book = 0
        export_book = 0

        add_client = 0
        edit_client = 0
        delete_client = 0
        import_client = 0
        export_client = 0

        add_branch = 0
        add_publisher = 0
        add_author = 0
        add_category = 0
        add_employee = 0
        edit_employee = 0


            ## ADMIN
        if self.checkBox_23.isChecked():#admin checkBox
            is_admin = 1
            books_tab = 1
            clients_tab = 1
            dashboard_tab = 1
            history_tab = 1
            reports_tab = 1
            settings_tab = 1

            add_book = 1
            edit_book = 1
            delete_book = 1
            import_book = 1
            export_book = 1

            add_client = 1
            edit_client = 1
            delete_client = 1
            import_client = 1
            export_client = 1

            add_branch = 1
            add_publisher = 1
            add_author = 1
            add_category = 1
            add_employee = 1
            edit_employee = 1

        else:
                ## TABS
            if self.checkBox_7.isChecked():
                books_tab = 1
            if self.checkBox_8.isChecked():
                clients_tab = 1
            if self.checkBox_9.isChecked():
                dashboard_tab = 1
            if self.checkBox_10.isChecked():
                history_tab = 1
            if self.checkBox_11.isChecked():
                reports_tab = 1
            if self.checkBox_12.isChecked():
                settings_tab = 1
                ## BOOKS
            if self.checkBox.isChecked():
                add_book = 1
            if self.checkBox_2.isChecked():
                edit_book = 1
            if self.checkBox_3.isChecked():
                delete_book = 1
            if self.checkBox_13.isChecked():
                import_book = 1
            if self.checkBox_14.isChecked():
                export_book = 1

                ## ClIENTS
            if self.checkBox_4.isChecked():
                add_client = 1
            if self.checkBox_6.isChecked():
                edit_client = 1
            if self.checkBox_6.isChecked():
                delete_client = 1
            if self.checkBox_16.isChecked():
                import_client = 1
            if self.checkBox_15.isChecked():
                export_client = 1

                ## SETTINGS
            if self.checkBox_17.isChecked():
                add_branch = 1
            if self.checkBox_18.isChecked():
                add_publisher = 1
            if self.checkBox_19.isChecked():
                add_author = 1
            if self.checkBox_21.isChecked():
                add_category = 1
            if self.checkBox_20.isChecked():
                employee_name = 1
            if self.checkBox_22.isChecked():
                edit_employee = 1


        self.cur.execute('''
            INSERT INTO employee_permissions  (employee_name, books_tab, clients_tab, dashboard_tab, history_tab,
                                                reports_tab, settings_tab,
                                                add_book,edit_book,delete_book,import_book,export_book,
                                                add_client,edit_client,delete_client,import_client,export_client,
                                                add_branch,add_publisher,add_author,add_category,add_employee,edit_employee,is_admin)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (employee_name, books_tab, clients_tab, dashboard_tab, history_tab, reports_tab, settings_tab,
              add_book,edit_book,delete_book,import_book,export_book,
              add_client,edit_client,delete_client,import_client,export_client,
              add_branch,add_publisher,add_author,add_category,add_employee,edit_employee,is_admin))

        self.db.commit()
        print("Permissions Added")
        self.statusBar().showMessage("تم اصاقة الصلاحيات للموظف بنجاح")
        self.PopUpMessage("تم اضافة الصلاحيات للموظف بنجاح", "success")

    def Admin_Report(self):
        ## Send Report To the Admin
        pass

    #######################################################3
    #########################################################
    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)
        print('Login Tab')

    def Open_Reset_Password_Tab(self):
        self.tabWidget.setCurrentIndex(1)
        print('Reset Password Tab')


    def Open_Daily_movements_Tab(self):
        self.tabWidget.setCurrentIndex(2)       # this for the head bar that we hide it with code  ==> the bar that contains page tab1 tab2 page , ... etc
        print('Daily Movements Tab')

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(0)
        print('Books Tab')

    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)
        print('Clients Tab')

    def Open_Dahsboard_Tab(self):

        self.get_dashboard_data()
        self.tabWidget.setCurrentIndex(5)
        print('Dashboard Tab')

    def Open_History_Tab(self):
        self.tabWidget.setCurrentIndex(6)
        print('History Tab')

    def Open_Reports_Tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)
        print('Reports Tab')

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)
        print('Settings Tab')
    def Show_Password(self):
        self.lineEdit_39.setEchoMode(QLineEdit.Normal)
        self.pushButton_48.setText("hide")
        self.pushButton_48.clicked.connect(self.Hide_Password)

    def Hide_Password(self):
        self.pushButton_48.setText("see")
        self.lineEdit_39.setEchoMode(QLineEdit.Password)

    def User_Login_permissions(self):
        username = self.lineEdit_38.text()
        username_ = hashlib.sha256(username.encode('utf-8')).hexdigest()
        password = self.lineEdit_39.text()
        password_ = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # print("Username ", type(username))
        # print("Password ", type(password))
        self.Open_Daily_movements_Tab()
        sql = '''SELECT id, mail, password, branch from employee WHERE 1=1'''
        # sql = '''SELECT id, mail, phone, national_id from employee WHERE 1=1'''
        self.cur.execute(sql)
        data = self.cur.fetchall()

        # the following lines to enable admin to use app before creating database;
        if (username_ == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918") and (password_ == "9360f05a8d7d56ee44001d9367dff2e053945a14b19d8fab6c8ec43d3796833c"):
            # print(username, "\t", password)
            self.pushButton.setEnabled(True)        # Today
            self.pushButton_2.setEnabled(True)      # Books
            self.pushButton_3.setEnabled(True)      # Clients
            self.pushButton_4.setEnabled(True)      # Dashboard
            self.pushButton_6.setEnabled(True)      # History
            self.pushButton_7.setEnabled(True)      # Reports
            self.pushButton_5.setEnabled(True)      # Settings
            self.pushButton_10.setEnabled(True)     # Add               ==> in add new book tab
            self.pushButton_13.setEnabled(True)     # Save Book         ==> Edit or Delete book
            self.pushButton_15.setEnabled(True)     # Delete            ==> Edit or Delete book
            self.pushButton_34.setEnabled(True)     # Import            ==> All Books
            self.pushButton_35.setEnabled(True)     # Export            ==> All Books
            self.pushButton_17.setEnabled(True)     # Add Client        ==> in add client tab
            self.pushButton_18.setEnabled(True)     # Save Client Data  ==> in Edit or Delete Client
            self.pushButton_27.setEnabled(True)     # Delete            ==> in Edit or Delete Client
            self.pushButton_36.setEnabled(True)     # Import            ==> in add client tab
            self.pushButton_37.setEnabled(True)     # Export            ==> in add client tab
            self.pushButton_20.setEnabled(True)     # Add Branch        ==> Add Data Tab
            self.pushButton_21.setEnabled(True)     # Add Publisher     ==> Add Data Tab
            self.pushButton_22.setEnabled(True)     # Add Author        ==> Add Data Tab
            self.pushButton_23.setEnabled(True)     # Add Category      ==> Add Data Tab
            self.pushButton_26.setEnabled(True)     # Add employee      ==> in add employee tab
            self.pushButton_28.setEnabled(True)     # Save              ==> in add employee tab

        for row in data:
            if row[1] == username and row[2] == password:
                # print(row[0])
                global employee_id, employee_branch
                employee_id = row[0]
                employee_branch = row[3]

                date = datetime.datetime.now()
                action = 0
                table = 6
                try:
                    self.cur.execute('''
                        INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch_id,data)
                        VALUES(%s,%s,%s,%s,%s,%s)
                    ''', (employee_id, action, table, date, employee_branch,username))
                except:
                    pass
                self.db.commit()
                self.Show_History()

                ## load user permissions
                self.groupBox_14.setEnabled(True)
                self.cur.execute('''
                        SELECT * FROM employee_permissions WHERE employee_name=%s
                ''',(username,))
                user_permissions = self.cur.fetchall()
                self.pushButton.setEnabled(True)

                if user_permissions[0][2] == 1: ## Book Tab
                    self.pushButton_2.setEnabled(True)
                if user_permissions[0][3] == 1: ## Clients Tab
                    self.pushButton_3.setEnabled(True)
                if user_permissions[0][4] == 1: ## Dashboard Tab
                    self.pushButton_4.setEnabled(True)
                if user_permissions[0][5] == 1: ## History Tab
                    self.pushButton_6.setEnabled(True)

                if user_permissions[0][6] == 1: ## Reports Tab
                    self.pushButton_7.setEnabled(True)
                if user_permissions[0][7] == 1: ## Settings Tab
                    self.pushButton_5.setEnabled(True)
                if user_permissions[0][8] == 1: ## Add Book
                    self.pushButton_10.setEnabled(True)
                if user_permissions[0][9] == 1: ## Edit Book
                    self.pushButton_13.setEnabled(True)

                if user_permissions[0][10] == 1:  ## Delete Book
                    self.pushButton_15.setEnabled(True)
                if user_permissions[0][11] == 1:  ## Import Books
                    self.pushButton_34.setEnabled(True)
                if user_permissions[0][12] == 1:  ## Export Book
                    self.pushButton_35.setEnabled(True)
                if user_permissions[0][13] == 1:  ## Add Client
                    self.pushButton_17.setEnabled(True)

                if user_permissions[0][14] == 1:  ## Edit Client
                    self.pushButton_18.setEnabled(True)
                if user_permissions[0][15] == 1:  ## Delete Client
                    self.pushButton_27.setEnabled(True)
                if user_permissions[0][16] == 1:  ## Import Client
                    self.pushButton_36.setEnabled(True)
                if user_permissions[0][17] == 1:  ## Export Client
                    self.pushButton_37.setEnabled(True)

                if user_permissions[0][18] == 1:  ## Add branch
                    self.pushButton_20.setEnabled(True)
                if user_permissions[0][19] == 1:  ## Add Publisher
                    self.pushButton_21.setEnabled(True)
                if user_permissions[0][20] == 1:  ## Add Author
                    self.pushButton_22.setEnabled(True)
                if user_permissions[0][21] == 1:  ## Add Category
                    self.pushButton_23.setEnabled(True)

                if user_permissions[0][22] == 1:  ## Add Employee
                    self.pushButton_26.setEnabled(True)
                if user_permissions[0][23] == 1:  ## Save Employee
                    self.pushButton_28.setEnabled(True)

            ## The following code get an error and show password is incorrect always

            # elif row[1] != username and row[2] != password:
            #     self.PopUpMessage("اسم المستخدم او كلمة المرور غير صحيح\n Username or password is incorrect try again", "Error")
            #     # self.PopUpMessage("اسم المستخدم او كلمة المرور غير صحيح", "Error")
            #     self.Open_Login_Tab()
            #     break
                # QMessageBox.information(self,)
######################################## DashBoard
######################################## DashBoard

    def get_dashboard_data(self):
        ## Retreive data
        filter_date = self.dateEdit_8.date()
        filter_date = filter_date.toPyDate()
        year = str(filter_date).split('-')[0]

        # sql = '''SELECT book_id, Book_from from daily_movement'''
        self.cur.execute(''' SELECT COUNT(book_id), EXTRACT(MONTH FROM Book_to) as month
                            FROM daily_movement
                            WHERE year(Book_to) = %s
                            GROUP BY month
        ''' %(year))
        print(year)

        data = self.cur.fetchall()

        pen = pg.mkPen(color=(255,0,0))
        books_count = []
        rent_count = []
        for row in data:
            books_count.append(row[0])
            rent_count.append(row[1])

        # self.widget.plot(books_count,rent_count,pen=pen, symbol='+', symbolSize=20,synboleBrush=('w'))
        barchart = pg.BarGraphItem(x=rent_count, height=books_count, width=0.2)
        self.widget.addItem(barchart)


        # self.widget.setBackground('w') ## to change the bacjground
        self.widget.setTitle('المبيعات') ## size="30")
        self.widget.addLegend()
        self.widget.setLabel('left', 'الشهر', color='red', size=40)
        self.widget.setLabel('bottom', 'عدد الكتب المعارة', color='red', size=40)
        self.widget.showGrid(x=True, y=True)


######################################## DashBoard

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
