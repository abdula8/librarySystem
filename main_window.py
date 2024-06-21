from PyQt5.QtWidgets import QMainWindow
from ui.ui_main_window import Ui_MainWindow
from db_operations import DbOperations
from ui_operations import UiOperations
from book_operations import BookOperations
from client_operations import ClientOperations
from employee_operations import EmployeeOperations
from report_operations import ReportOperations
# from login_dialog import LoginDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.db_ops = DbOperations()
        self.ui_ops = UiOperations(self)
        self.book_ops = BookOperations(self)
        self.client_ops = ClientOperations(self)
        self.employee_ops = EmployeeOperations(self)
        self.report_ops = ReportOperations(self)
        # Connect the logout action to the logout method
        # self.actionLogout.triggered.connect(self.logout)
        self.username = username
        self.init_ui()

    def init_ui(self):
        # self.employee_ops.user_login_permissions(self.username)
        self.setWindowTitle("Main Window")
        self.disable_all_buttons()
        self.load_user_permissions()
        self.disable_tabwidgets()
        self.show_branches()
        self.show_employee()

    
    # def logout(self):
    #     # Implement the logout functionality here
    #     self.db_ops.close_connection()
    #     self.close()
    #     self.login_dialog = LoginDialog()
    #     self.login_dialog.exec_()

    def disable_tabwidgets(self):
        ## UI_Changes in login
        # the code to hide the tab bar
        self.tabWidget.tabBar().setVisible(False)
        # self.tabWidget_2.tabBar().setVisible(False)

    def disable_all_buttons(self):
        buttons = [
            self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
            self.pushButton_5, self.pushButton_6, self.pushButton_7, self.pushButton_10,
            self.pushButton_13, self.pushButton_15, self.pushButton_34, self.pushButton_35,
            self.pushButton_17, self.pushButton_18, self.pushButton_27, self.pushButton_36,
            self.pushButton_37, self.pushButton_20, self.pushButton_21, self.pushButton_22,
            self.pushButton_23, self.pushButton_26, self.pushButton_28
        ]
        for btn in buttons:
            btn.setEnabled(False)

    def load_user_permissions(self):
        user_permissions = self.employee_ops.get_user_permissions(self.username)
        if user_permissions:
            self.handle_buttons(user_permissions)
    
    def handle_buttons(self, permissions):
        
        # default tab to open on...
        self.pushButton.setEnabled(True)
        self.open_daily_movements_tab()
        self.pushButton.clicked.connect(self.open_daily_movements_tab)

        if permissions['book_tab']:
            self.pushButton_2.setEnabled(True)
            self.pushButton_2.clicked.connect(self.open_book_tab)
        if permissions['clients_tab']:
            self.pushButton_3.setEnabled(True)
            self.pushButton_3.clicked.connect(self.open_clients_tab)
        if permissions['dashboard_tab']:
            self.pushButton_4.setEnabled(True)
            self.pushButton_4.clicked.connect(self.open_dashboard_tab)
        if permissions['history_tab']:
            self.pushButton_6.setEnabled(True)
            self.pushButton_6.clicked.connect(self.open_history_tab)
        if permissions['reports_tab']:
            self.pushButton_7.setEnabled(True)
            self.pushButton_7.clicked.connect(self.open_reports_tab)
        if permissions['settings_tab']:
            self.pushButton_5.setEnabled(True)
            self.pushButton_5.clicked.connect(self.open_settings_tab)
        if permissions['add_book']:
            self.pushButton_10.setEnabled(True)
            self.pushButton_10.clicked.connect(self.add_book)
        if permissions['edit_book']:
            self.pushButton_13.setEnabled(True)
            self.pushButton_13.clicked.connect(self.edit_book)
        if permissions['delete_book']:
            self.pushButton_15.setEnabled(True)
            self.pushButton_15.clicked.connect(self.delete_book)
        if permissions['import_books']:
            self.pushButton_34.setEnabled(True)
            self.pushButton_34.clicked.connect(self.import_books)
        if permissions['export_books']:
            self.pushButton_35.setEnabled(True)
            self.pushButton_35.clicked.connect(self.export_books)
        if permissions['add_client']:
            self.pushButton_17.setEnabled(True)
            self.pushButton_17.clicked.connect(self.add_client)
        if permissions['edit_client']:
            self.pushButton_18.setEnabled(True)
            self.pushButton_18.clicked.connect(self.edit_client)
        if permissions['delete_client']:
            self.pushButton_27.setEnabled(True)
            self.pushButton_27.clicked.connect(self.delete_client)
        if permissions['import_clients']:
            self.pushButton_36.setEnabled(True)
            self.pushButton_36.clicked.connect(self.import_clients)
        if permissions['export_clients']:
            self.pushButton_37.setEnabled(True)
            self.pushButton_37.clicked.connect(self.export_clients)
        if permissions['add_branch']:
            self.pushButton_20.setEnabled(True)
            self.pushButton_20.clicked.connect(self.add_branch)
        if permissions['add_publisher']:
            self.pushButton_21.setEnabled(True)
            self.pushButton_21.clicked.connect(self.add_publisher)
        if permissions['add_author']:
            self.pushButton_22.setEnabled(True)
            self.pushButton_22.clicked.connect(self.add_author)
        if permissions['add_category']:
            self.pushButton_23.setEnabled(True)
            self.pushButton_23.clicked.connect(self.add_category)
        if permissions['add_employee']:
            self.pushButton_26.setEnabled(True)
            # self.pushButton_26.clicked.connect(self.add_employee)
            self.pushButton_26.clicked.connect(self.employee_ops.add_employee)
        if permissions['save_employee']:
            self.pushButton_28.setEnabled(True)
            self.pushButton_28.clicked.connect(self.save_employee)

    # def Open_Login_Tab(self):
    #     self.tabWidget.setCurrentIndex(0)
    #     print('Login Tab')

    # def Open_Reset_Password_Tab(self):
    #     self.tabWidget.setCurrentIndex(1)
    #     print('Reset Password Tab')
    
    ''''
    tabWidget:
        this for the head bar that we hide it with code 
        ==> the bar that contains page tab1 tab2 page , ... etc
    tabWidget_2:
        for the second head bar
    '''
    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(3)   
        self.tabWidget_2.setCurrentIndex(0)
        print('Book tab!!')

    def open_clients_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)
        print('Clients tab!!')

    def open_dashboard_tab(self):
        # self.get_dashboard_data()
        self.tabWidget.setCurrentIndex(5)
        print('Dashboard Tab')
        print('Dashboard tab!!')

    def open_history_tab(self):
        self.tabWidget.setCurrentIndex(6)
        print('History tab!!')

    def open_reports_tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)
        print('Reports tab!!')

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)
        print('Settings tab!!')

    def Show_All_Categories(self):
        self.comboBox_7.clear()
        self.comboBox_3.clear()
        self.comboBox_13.clear()
        self.comboBox_2.clear()
        # Get category ID
        sql = ('''SELECT id FROM category''')
        categories = self.db_ops.execute_query(sql) # to fetchall() data from database
        if categories:
            categories = sorted([cat[0] for cat in categories])  # Flatten the list of tuples

            for category_id in categories:
                sql = '''SELECT category FROM category WHERE id=%s'''
                param = (category_id,)
                category_name = self.db_ops.execute_query(sql, param)
                
                if category_name:
                    category_name = category_name[0][0]  # Extract the category name from the tuple
                    self.comboBox_7.addItem(category_name)
                    self.comboBox_3.addItem(category_name)
                    self.comboBox_13.addItem(category_name)
                    self.comboBox_2.addItem(category_name)

    def add_book(self):
        pass

    def edit_book(self):
        pass

    def delete_book(self):
        pass

    def import_books(self):
        pass

    def export_books(self):
        pass

    def add_client(self):
        ## add new Client
        client_name         = self.lineEdit_14.text()
        client_email        = self.lineEdit_15.text()
        client_phone        = self.lineEdit_16.text()
        client_national_id  = self.lineEdit_17.text()
        import re
        from datetime import datetime
        date = datetime.now()

        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # mail_pattern = re.match(r'^[a-zA-Z][\w\-.]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$', client_email)
        mail_pattern = re.match(email_pattern, client_email)
        phon_pattern = re.match(r'^01[\d]{9}$', str(client_phone))
        naID_pattern = re.match(r'^[\d]{14}$', str(client_national_id))
        sql = ('''INSERT INTO clients(name, mail, phone, national_id, date)
                VALUES (%s,%s,%s,%s,%s)''')
        param = (client_name, client_email, client_phone, client_national_id, date)
        if mail_pattern and phon_pattern and naID_pattern:
            self.db_ops.execute_query(sql, param)
            self.db_ops.commit()
            print("Client added")
            self.statusBar().showMessage("تم إضافة العميل بنجاح")
            self.ui_ops.pop_up_message("تم إضافة العميل بنجاح", "Password Correct")
            # import time
            # time.sleep(1)
            ## add new Client
            client_name         = self.lineEdit_14.setText('')
            client_email        = self.lineEdit_15.setText('')
            client_phone        = self.lineEdit_16.setText('')
            client_national_id  = self.lineEdit_17.setText('')


    def edit_client(self):
        pass

    def delete_client(self):
        pass

    def import_clients(self):
        pass

    def export_clients(self):
        pass

    def add_branch(self):
        ## add new  branch
        branch_name = self.lineEdit_23.text()
        branch_code = self.lineEdit_24.text()
        branch_location = self.lineEdit_25.text()

        sql = ('''INSERT INTO branch (name, code, location)
                  VALUES(%s, %s, %s)''')
        param = (branch_name, branch_code, branch_location)
        self.db_ops.execute_query(sql, params=param)
        self.db_ops.commit()
        print('Branch Added')


    def add_publisher(self):

        ## add new puplisher
        publisher_name = self.lineEdit_26.text()
        publisher_location = self.lineEdit_28.text()

        sql = '''INSERT INTO publisher (name, location)
                 VALUES(%s, %s)
              '''
        param = (publisher_name, publisher_location)
        self.db_ops.execute_query(sql, params=param)
        self.db_ops.commit()
        # from datetime import datetime
        # date = datetime.now()
        # global employee_id, employee_branch
        # action = 2
        # table = 7
        # self.cur.execute('''
        #        INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch,data)
        #        VALUES(%s,%s,%s,%s,%s,%s)
        #    ''', (employee_id, action, table, date, employee_branch, publisher_name))
        # self.Show_History()

        # self.db.commit() # to save data on hard disk not only ram
        print('Publisher Added')
        self.lineEdit_26.text()
        self.lineEdit_28.text()

    def add_author(self):
        pass

    def add_category(self):
        category_name = self.lineEdit_30.text()
        # I deleted code of parent category
        if category_name:
            sql = '''INSERT INTO category (category) VALUES (%s)'''
            param = (category_name,)
            self.db_ops.execute_query(sql, param)
            self.db_ops.commit()
            print('Category Added')
            self.lineEdit_30.setText('')
            self.Show_All_Categories()
        else:
            print('Category name is empty')

    def add_employee(self):
        pass
    
    def save_employee(self):
        pass

    def show_employee(self):
        sql = '''SELECT mail FROM employee'''
        employees = self.db_ops.execute_query(sql)
        # self.cur.execute('''SELECT mail FROM employee''')
        # employees = self.cur.fetchall()
        for employee in employees:
            self.comboBox_18.addItem(employee[0])
            self.comboBox_10.addItem(employee[0])

    def show_branches(self):
        sql = '''SELECT name FROM branch'''
        branches = self.db_ops.execute_query(sql)
        # self.cur.execute('''SELECT name FROM branch''')
        # branches = self.cur.fetchall()
        for branch in branches:
            self.comboBox_21.addItem(branch[0])
            self.comboBox_22.addItem(branch[0])
    def open_daily_movements_tab(self):
        self.tabWidget.setCurrentIndex(2)       # this for the head bar that we hide it with code  ==> the bar that contains page tab1 tab2 page , ... etc
        print('Daily Movements Tab')