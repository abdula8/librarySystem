from PyQt5.QtWidgets import QDialog, QMessageBox
from ui.ui_login_dialog import Ui_LoginDialog
from employee_operations import EmployeeOperations
from db_operations import DbOperations  # Import DbOperations

class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db_ops = DbOperations()  # Initialize DbOperations
        self.employee_ops = EmployeeOperations(self.db_ops)
        # self.pushButton_login.clicked.connect(self.handle_login)
        self.loginButton.clicked.connect(self.handle_login)
        self.username = None

    def handle_login(self):
        # username = self.lineEdit_username.text()
        # password = self.lineEdit_password.text()
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        if self.employee_ops.verify_login(username, password):
            self.username = username
            self.accept()
        else:
            # self.label_error.setText("Invalid username or password.")
            QMessageBox.warning(self, 'Error', 'Bad user or password')
    
    # def authenticate(self, username, password):
    #     # Placeholder authentication logic
    #     admin_username_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
    #     admin_password_hash = "9360f05a8d7d56ee44001d9367dff2e053945a14b19d8fab6c8ec43d3796833c"
    #     return username == admin_username_hash and password == admin_password_hash
