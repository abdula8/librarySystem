import sys
from PyQt5 import QtWidgets, uic

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        uic.loadUi('login_dialog.ui', self)
        self.loginButton = self.findChild(QtWidgets.QPushButton, 'loginButton')
        self.usernameInput = self.findChild(QtWidgets.QLineEdit, 'usernameInput')
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, 'passwordInput')
        self.loginButton.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        if self.authenticate(username, password):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password')

    def authenticate(self, username, password):
        # Placeholder authentication logic
        return username == 'admin' and password == 'admin'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main.ui', self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    login_dialog = LoginDialog()
    if login_dialog.exec() == QtWidgets.QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
