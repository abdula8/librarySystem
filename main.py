
import logging

logging.basicConfig(level=logging.INFO)

# Your existing imports and code
from PyQt5.QtWidgets import QApplication
import sys
from main_window import MainWindow
from login_dialog import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    login_dialog = LoginDialog()
    if login_dialog.exec_() == LoginDialog.Accepted:
        main_win = MainWindow(login_dialog.username)
        main_win.show()
        
    sys.exit(app.exec_())
