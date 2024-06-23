from PyQt5.QtWidgets import QMessageBox

class UiOperations:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_ui(self):
        self.main_window.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.main_window.pushButton.clicked.connect(self.main_window.ui_ops.open_daily_movements_tab)
        self.main_window.pushButton_2.clicked.connect(self.main_window.ui_ops.open_books_tab)
        self.main_window.pushButton_3.clicked.connect(self.main_window.ui_ops.open_clients_tab)
        self.main_window.pushButton_4.clicked.connect(self.main_window.ui_ops.open_dashboard_tab)
        self.main_window.pushButton_6.clicked.connect(self.main_window.ui_ops.open_history_tab)
        self.main_window.pushButton_7.clicked.connect(self.main_window.ui_ops.open_reports_tab)
        self.main_window.pushButton_5.clicked.connect(self.main_window.ui_ops.open_settings_tab)

        self.main_window.pushButton_20.clicked.connect(self.main_window.book_ops.add_branch)
        self.main_window.pushButton_21.clicked.connect(self.main_window.book_ops.add_publisher)
        self.main_window.pushButton_22.clicked.connect(self.main_window.book_ops.add_author)
        self.main_window.pushButton_23.clicked.connect(self.main_window.book_ops.add_category)
        self.main_window.pushButton_26.clicked.connect(self.main_window.employee_ops.add_employee)

        self.main_window.pushButton_10.clicked.connect(self.main_window.book_ops.add_new_book)
        self.main_window.pushButton_14.clicked.connect(self.main_window.book_ops.edit_book_search)
        self.main_window.pushButton_13.clicked.connect(self.main_window.book_ops.edit_book)
        self.main_window.pushButton_15.clicked.connect(self.main_window.book_ops.delete_book)
        self.main_window.pushButton_9.clicked.connect(self.main_window.book_ops.all_book_filter)
        self.main_window.pushButton_35.clicked.connect(self.main_window.book_ops.books_export_report)

        self.main_window.pushButton_17.clicked.connect(self.main_window.client_ops.add_new_client)
        self.main_window.pushButton_19.clicked.connect(self.main_window.client_ops.edit_client_search)
        self.main_window.pushButton_18.clicked.connect(self.main_window.client_ops.edit_client)
        self.main_window.pushButton_27.clicked.connect(self.main_window.client_ops.delete_client)
        self.main_window.pushButton_37.clicked.connect(self.main_window.client_ops.client_export_report)

        self.main_window.pushButton_8.clicked.connect(self.main_window.ui_ops.handle_to_day_work)
        self.main_window.pushButton_29.clicked.connect(self.main_window.employee_ops.check_employee)
        self.main_window.pushButton_28.clicked.connect(self.main_window.employee_ops.edit_employee_data)
        self.main_window.pushButton_30.clicked.connect(self.main_window.employee_ops.add_employee_permissions)
        self.main_window.checkBox_23.clicked.connect(self.main_window.employee_ops.check_employee_permissions)
        self.main_window.pushButton_38.clicked.connect(self.main_window.employee_ops.user_login_permissions)
        # self.main_window.pushButton_48.clicked.connect(self.main_window.employee_ops.show_password)
        self.main_window.pushButton_42.clicked.connect(self.main_window.ui_ops.get_dashboard_data)

    # Chat GPT Work
    def open_daily_movements_tab(self):
        self.main_window.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.main_window.tabWidget.setCurrentIndex(1)

    def open_clients_tab(self):
        self.main_window.tabWidget.setCurrentIndex(2)

    def open_dashboard_tab(self):
        self.main_window.tabWidget.setCurrentIndex(3)

    def open_history_tab(self):
        self.main_window.tabWidget.setCurrentIndex(4)

    def open_reports_tab(self):
        self.main_window.tabWidget.setCurrentIndex(5)

    def open_settings_tab(self):
        self.main_window.tabWidget.setCurrentIndex(6)

    def handle_to_day_work(self):
        pass

    def get_dashboard_data(self):
        pass

    def pop_up_message(self, parent, message, title, action):
        if action == "delete":
            msg = QMessageBox.question(parent, title, message, QMessageBox.Yes| QMessageBox.No)
            if msg == QMessageBox.Yes:
                return True
            elif msg == QMessageBox.No:
                return False
        else:
            msg = QMessageBox()
            msg.setWindowTitle(title)
            msg.setText(message)
            x = msg.exec_()
'''
    # My Work
    def Open_Login_Tab(self):
        self.main_window.tabWidget.setCurrentIndex(0)
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
'''