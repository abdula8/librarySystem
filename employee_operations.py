import hashlib
from datetime import datetime
from db_operations import DbOperations

class EmployeeOperations:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db_ops = DbOperations()

    def add_employee(self):
        # employee_name = self.main_window.lineEdit_29.text()
        # employee_email = self.main_window.lineEdit_30.text()
        # employee_phone = self.main_window.lineEdit_31.text()
        # employee_branch = self.main_window.lineEdit_32.text()
        # employee_status = self.main_window.comboBox_15.currentIndex()

        # Retrieve data from input fields
        employee_name = self.main_window.lineEdit_33.text()
        employee_mail = self.main_window.lineEdit_27.text()
        employee_phone = self.main_window.lineEdit_32.text()
        employee_branch = self.main_window.comboBox_21.currentIndex()
        national_id = self.main_window.lineEdit_34.text()
        priority = self.main_window.lineEdit_35.text()
        password = self.main_window.lineEdit_37.text()
        password_2 = self.main_window.lineEdit_52.text()

        date = datetime.now()

        # Check if passwords match
        if password == password_2:
            sql = ('''
                INSERT INTO employee (name, mail, phone, date, national_id, priority, password, branch)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            ''')
            params = (employee_name, employee_mail, employee_phone, date, national_id, priority, password, employee_branch)
            self.db_ops.execute_query(sql, params)
            self.db_ops.commit()

            # Clear the input fields
            self.main_window.lineEdit_33.setText('')
            self.main_window.lineEdit_27.setText('')
            self.main_window.lineEdit_32.setText('')
            self.main_window.lineEdit_34.setText('')
            self.main_window.lineEdit_35.setText('')
            self.main_window.lineEdit_37.setText('')
            self.main_window.lineEdit_52.setText('')

            # Show success message
            self.main_window.statusBar().showMessage("تم إضافة الموظف بنجاح")
            self.main_window.ui_ops.pop_up_message("تم إضافة الموظف بنجاح", "Password Correct")
        else:
            print("Wrong Password!!")
            self.main_window.ui_ops.pop_up_message("Your passwords don't match. Please enter the second one again.", "Password Error")
            self.main_window.lineEdit_37.setText('')  # password
            self.main_window.lineEdit_52.setText('')  # password_2

        # query = '''
        #     INSERT INTO employees(name, email, phone, branch, status)
        #     VALUES (%s, %s, %s, %s, %s)
        # '''
        # query = '''INSERT INTO employee (name, mail, phone, date, national_id, priority, password, branch)
        #            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
        # params = (employee_name, employee_email, employee_phone, date, national_id, priority, password, employee_branch)
        # self.db_ops.execute_query(query, params)
        # self.db_ops.commit()

        # self.main_window.ui_ops.pop_up_message("تم إضافة الموظف", "عملية صحيحة")
        # self.main_window.lineEdit_29.setText('')
        # self.main_window.lineEdit_30.setText('')
        # self.main_window.lineEdit_31.setText('')
        # self.main_window.lineEdit_32.setText('')

    def check_employee(self):
        employee_id = self.main_window.lineEdit_33.text()
        query = 'SELECT * FROM employees WHERE id = %s'
        employee = self.db_ops.execute_query(query, (employee_id,))

        if employee:
            self.main_window.lineEdit_34.setText(employee[0][1])
            self.main_window.lineEdit_35.setText(employee[0][2])
            self.main_window.lineEdit_36.setText(employee[0][3])
            self.main_window.comboBox_16.setCurrentIndex(int(employee[0][5]))

    def edit_employee_data(self):
        employee_id = self.main_window.lineEdit_33.text()
        employee_name = self.main_window.lineEdit_34.text()
        employee_email = self.main_window.lineEdit_35.text()
        employee_phone = self.main_window.lineEdit_36.text()
        employee_branch = self.main_window.lineEdit_37.text()
        employee_status = self.main_window.comboBox_16.currentIndex()

        query = '''
            UPDATE employees SET name=%s,email=%s,phone=%s,branch=%s,status=%s WHERE id = %s
        '''
        params = (employee_name, employee_email, employee_phone, employee_branch, employee_status, employee_id,)
        self.db_ops.execute_query(query, params) # Edited from mainwindow.db_ops to db_ops
        self.db_ops.commit() # Edited from mainwindow.db_ops to db_ops

        self.main_window.ui_ops.pop_up_message("تم تعديل بيانات الموظف", "عملية صحيحة")

    def add_employee_permissions(self):
        employee_id = self.main_window.lineEdit_33.text()
        permissions = []

        if self.main_window.checkBox_23.isChecked():
            permissions.append(1)
        if self.main_window.checkBox_24.isChecked():
            permissions.append(2)
        if self.main_window.checkBox_25.isChecked():
            permissions.append(3)
        if self.main_window.checkBox_26.isChecked():
            permissions.append(4)

        for permission in permissions:
            query = '''
                INSERT INTO employee_permissions(employee_id, permission_id)
                VALUES (%s, %s)
            '''
            params = (employee_id, permission)
            self.db_ops.execute_query(query, params) # Edited from mainwindow.db_ops to db_ops

        self.db_ops.commit()
        self.main_window.ui_ops.pop_up_message("تم إضافة صلاحيات الموظف", "عملية صحيحة")

    def check_employee_permissions(self):
        pass


    def verify_login(self, username, password):
        username_hashed = hashlib.sha256(username.encode('utf-8')).hexdigest()
        password_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # sql = 'SELECT id, mail, password, branch FROM employee WHERE 1=1'
        sql = "SELECT id, mail, password, branch FROM employee WHERE mail=%s AND password=%s"
        # data = self.db_ops.execute_query(sql, (username_hashed, password_hashed))
        data = self.db_ops.execute_query(sql, (username, password))
        # param = (username, password)
        # self.main_window.db_ops.cur.execute(sql)
        
        # self.db_ops.execute_query(sql) # Edited from mainwindow.execute_query to db_ops.execute_query
        
        # data = self.main_window.db_ops.cur.fetchall()
        
        # data = self.db_ops.execute_query(sql) # Edited from mainwindow.execute_query to db_ops.execute_query
        # data = self.db_ops.execute_query(sql, param)

        admin_username_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
        admin_password_hash = "9360f05a8d7d56ee44001d9367dff2e053945a14b19d8fab6c8ec43d3796833c"

        if username_hashed == admin_username_hash and password_hashed == admin_password_hash:
            return True

        for row in data:
            if row[1] == username and row[2] == password:
                return True

        return False

    def user_login_permissions(self, username):
        username_hashed = hashlib.sha256(username.encode('utf-8')).hexdigest()

        sql = 'SELECT id, mail, password, branch FROM employee  WHERE mail=%s' # changed from WHERE 1=1 to WHERE mail=%s
        self.db_ops.cur.execute(sql, (username,)) # Edited from mainwindow.db_ops to db_ops
        data = self.db_ops.cur.fetchall() # Edited from mainwindow.db_ops to db_ops

        # Admin access
        # admin_username_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"   #admin
        # admin_password_hash = "9360f05a8d7d56ee44001d9367dff2e053945a14b19d8fab6c8ec43d3796833c" # 512512
        
        # if username_hashed == admin_username_hash:
        #     self.enable_all_features()
        #     return

        for row in data:
            if row[1] == username:
                global employee_id, employee_branch
                employee_id = row[0]
                employee_branch = row[3]

                date = datetime.now()
                action = 0
                table = 6
                try:
                    self.db_ops.cur.execute('''
                        INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch_id, data)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (employee_id, action, table, date, employee_branch, username))
                except:
                    print("Error Occured!!!")

                self.db_ops.commit() # Edited from mainwindow.db_ops to db_ops
                self.main_window.ui_ops.show_history()

                self.load_user_permissions(username)

    def enable_all_features(self):
        self.main_window.pushButton.setEnabled(True)        # Today
        self.main_window.pushButton_2.setEnabled(True)      # Books
        self.main_window.pushButton_3.setEnabled(True)      # Clients
        self.main_window.pushButton_4.setEnabled(True)      # Dashboard
        self.main_window.pushButton_6.setEnabled(True)      # History
        self.main_window.pushButton_7.setEnabled(True)      # Reports
        self.main_window.pushButton_5.setEnabled(True)      # Settings
        self.main_window.pushButton_10.setEnabled(True)     # Add Book
        self.main_window.pushButton_13.setEnabled(True)     # Save Book
        self.main_window.pushButton_15.setEnabled(True)     # Delete Book
        self.main_window.pushButton_34.setEnabled(True)     # Import Books
        self.main_window.pushButton_35.setEnabled(True)     # Export Books
        self.main_window.pushButton_17.setEnabled(True)     # Add Client
        self.main_window.pushButton_18.setEnabled(True)     # Save Client
        self.main_window.pushButton_27.setEnabled(True)     # Delete Client
        self.main_window.pushButton_36.setEnabled(True)     # Import Clients
        self.main_window.pushButton_37.setEnabled(True)     # Export Clients
        self.main_window.pushButton_20.setEnabled(True)     # Add Branch
        self.main_window.pushButton_21.setEnabled(True)     # Add Publisher
        self.main_window.pushButton_22.setEnabled(True)     # Add Author
        self.main_window.pushButton_23.setEnabled(True)     # Add Category
        self.main_window.pushButton_26.setEnabled(True)     # Add Employee
        self.main_window.pushButton_28.setEnabled(True)     # Save Employee

    def load_user_permissions(self, username):
        self.main_window.groupBox_14.setEnabled(True)
        self.db_ops.cur.execute('''
            SELECT * FROM employee_permissions WHERE employee_name=%s
        ''', (username,)) # Edited from mainwindow.db_ops to db_ops
        user_permissions = self.db_ops.cur.fetchall() # Edited from mainwindow.db_ops to db_ops

        self.main_window.pushButton.setEnabled(True)

        permissions_mapping = {
            2: self.main_window.pushButton_2,
            3: self.main_window.pushButton_3,
            4: self.main_window.pushButton_4,
            5: self.main_window.pushButton_6,
            6: self.main_window.pushButton_7,
            7: self.main_window.pushButton_5,
            8: self.main_window.pushButton_10,
            9: self.main_window.pushButton_13,
            10: self.main_window.pushButton_15,
            11: self.main_window.pushButton_34,
            12: self.main_window.pushButton_35,
            13: self.main_window.pushButton_17,
            14: self.main_window.pushButton_18,
            15: self.main_window.pushButton_27,
            16: self.main_window.pushButton_36,
            17: self.main_window.pushButton_37,
            18: self.main_window.pushButton_20,
            19: self.main_window.pushButton_21,
            20: self.main_window.pushButton_22,
            21: self.main_window.pushButton_23,
            22: self.main_window.pushButton_26,
            23: self.main_window.pushButton_28,
        }

        for idx, button in permissions_mapping.items():
            if user_permissions[0][idx] == 1:
                button.setEnabled(True)
    
    def get_user_permissions(self, username):
        # username_hashed = hashlib.sha256(username.encode('utf-8')).hexdigest()

        sql = "SELECT * FROM employee_permissions WHERE employee_name=%s"
        permissions = self.db_ops.execute_query(sql, (username,))

        if permissions:
            return {
                'book_tab': permissions[0][2],
                'clients_tab': permissions[0][3],
                'dashboard_tab': permissions[0][4],
                'history_tab': permissions[0][5],
                'reports_tab': permissions[0][6],
                'settings_tab': permissions[0][7],
                'add_book': permissions[0][8],
                'edit_book': permissions[0][9],
                'delete_book': permissions[0][10],
                'import_books': permissions[0][11],
                'export_books': permissions[0][12],
                'add_client': permissions[0][13],
                'edit_client': permissions[0][14],
                'delete_client': permissions[0][15],
                'import_clients': permissions[0][16],
                'export_clients': permissions[0][17],
                'add_branch': permissions[0][18],
                'add_publisher': permissions[0][19],
                'add_author': permissions[0][20],
                'add_category': permissions[0][21],
                'add_employee': permissions[0][22],
                'save_employee': permissions[0][23],
            }
        return None