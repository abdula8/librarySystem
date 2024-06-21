# main.py
from user_management import UserManager
from book_management import BookManager
from borrowing_system import BorrowingSystem
from notifications import NotificationSystem
from reporting import Reporting

def main():
    user_manager = UserManager()
    book_manager = BookManager()
    borrowing_system = BorrowingSystem()
    notification_system = NotificationSystem()
    reporting = Reporting()

    # Example operations
    user_manager.add_user("John Doe", "johndoe@example.com")
    book_manager.add_book("The Great Gatsby", "F. Scott Fitzgerald", "123456789")
    borrowing_system.borrow_book("John Doe", "123456789")
    notification_system.send_notification("John Doe", "Your book is due in 3 days.")
    reporting.generate_report()

if __name__ == "__main__":
    main()
