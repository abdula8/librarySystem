from datetime import datetime

class BookOperations:
    def __init__(self, main_window):
        self.main_window = main_window

    def add_new_book(self):
        book_title = self.main_window.lineEdit_2.text()
        description = self.main_window.textEdit.toPlainText()
        category = self.main_window.comboBox_3.currentIndex()
        price = self.main_window.lineEdit_3.text()
        code = self.main_window.lineEdit_4.text()
        publisher = self.main_window.comboBox_4.currentIndex()
        author = self.main_window.comboBox_5.currentIndex()
        status = self.main_window.comboBox_6.currentIndex()
        part_order = self.main_window.lineEdit_36.text()
        barcode = self.main_window.lineEdit_40.text()
        date = datetime.now()

        query = '''
            INSERT INTO books(title,description,category_id,code,barcode,part_order,price,publisher_id,auther_id,status,date)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        params = (book_title, description, category, code, barcode, part_order, price, publisher, author, status, date)
        self.main_window.db_ops.execute_query(query, params)
        self.main_window.db_ops.commit()
        
        # Add history entry
        employee_id = 1  # Replace with actual employee ID
        employee_branch = 1  # Replace with actual employee branch
        action = 2
        table = 0
        history_query = '''
            INSERT INTO history (employee_id, employee_action, effected_table, operation_date, employee_branch, data)
            VALUES(%s,%s,%s,%s,%s,%s)
        '''
        history_params = (employee_id, action, table, date, employee_branch, book_title)
        self.main_window.db_ops.execute_query(history_query, history_params)
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم إضافة الكتاب الى قاعدة البيانات.", "عملية صحيحة")
        self.main_window.lineEdit_2.setText('')
        self.main_window.textEdit.setText('')
        self.main_window.lineEdit_3.setText('')
        self.main_window.lineEdit_4.setText('')
        self.main_window.lineEdit_36.setText('')
        self.main_window.lineEdit_40.setText('')

        self.show_all_books()

    def show_all_books(self):
        self.main_window.tableWidget_2.setRowCount(0)
        self.main_window.tableWidget_2.insertRow(0)

        query = 'SELECT code, title, category_id, auther_id, price FROM books'
        data = self.main_window.db_ops.execute_query(query)
        
        category_query = 'SELECT id FROM category'
        categories = sorted(self.main_window.db_ops.execute_query(category_query))

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 2:
                    category_query = 'SELECT category FROM category WHERE id=%s'
                    category_name = self.main_window.db_ops.execute_query(category_query, (categories[item],))
                    self.main_window.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))
                elif col == 3:
                    author_query = 'SELECT name FROM authors WHERE id=%s'
                    author_name = self.main_window.db_ops.execute_query(author_query, (item,))
                    self.main_window.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))
                else:
                    self.main_window.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1

            row_position = self.main_window.tableWidget_2.rowCount()
            self.main_window.tableWidget_2.insertRow(row_position)

    def add_branch(self):
        branch_name = self.main_window.lineEdit_25.text()
        query = 'INSERT INTO branch(name) VALUES (%s)'
        self.main_window.db_ops.execute_query(query, (branch_name,))
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم إضافة الفرع الى قاعدة البيانات", "عملية صحيحة")
        self.main_window.lineEdit_25.setText('')

    def add_publisher(self):
        publisher_name = self.main_window.lineEdit_26.text()
        query = 'INSERT INTO publisher(name) VALUES (%s)'
        self.main_window.db_ops.execute_query(query, (publisher_name,))
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم إضافة الناشر الى قاعدة البيانات", "عملية صحيحة")
        self.main_window.lineEdit_26.setText('')

    def add_author(self):
        author_name = self.main_window.lineEdit_27.text()
        query = 'INSERT INTO authors(name) VALUES (%s)'
        self.main_window.db_ops.execute_query(query, (author_name,))
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم إضافة المؤلف الى قاعدة البيانات", "عملية صحيحة")
        self.main_window.lineEdit_27.setText('')

    def add_category(self):
        category_name = self.main_window.lineEdit_28.text()
        query = 'INSERT INTO category(category) VALUES (%s)'
        self.main_window.db_ops.execute_query(query, (category_name,))
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم إضافة التصنيف الى قاعدة البيانات", "عملية صحيحة")
        self.main_window.lineEdit_28.setText('')

    def edit_book_search(self):
        code = self.main_window.lineEdit_5.text()
        query = 'SELECT * FROM books WHERE code = %s'
        book = self.main_window.db_ops.execute_query(query, (code,))

        if book:
            self.main_window.lineEdit_6.setText(book[0][1])
            self.main_window.textEdit_2.setPlainText(book[0][2])
            self.main_window.comboBox_9.setCurrentIndex(int(book[0][3]))
            self.main_window.lineEdit_8.setText(str(book[0][4]))
            self.main_window.lineEdit_9.setText(str(book[0][5]))
            self.main_window.comboBox_10.setCurrentIndex(int(book[0][7]))
            self.main_window.comboBox_11.setCurrentIndex(int(book[0][8]))
            self.main_window.comboBox_12.setCurrentIndex(int(book[0][9]))
            self.main_window.lineEdit_41.setText(str(book[0][10]))

    def edit_book(self):
        code = self.main_window.lineEdit_5.text()
        title = self.main_window.lineEdit_6.text()
        description = self.main_window.textEdit_2.toPlainText()
        category = self.main_window.comboBox_9.currentIndex()
        price = self.main_window.lineEdit_8.text()
        barcode = self.main_window.lineEdit_9.text()
        publisher = self.main_window.comboBox_10.currentIndex()
        author = self.main_window.comboBox_11.currentIndex()
        status = self.main_window.comboBox_12.currentIndex()
        part_order = self.main_window.lineEdit_41.text()
        date = datetime.now()

        query = '''
            UPDATE books SET title=%s, description=%s, category_id=%s, price=%s, barcode=%s,
            publisher_id=%s, auther_id=%s, status=%s, part_order=%s, date=%s WHERE code=%s
        '''
        params = (title, description, category, price, barcode, publisher, author, status, part_order, date, code)
        self.main_window.db_ops.execute_query(query, params)
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم تعديل بيانات الكتاب", "عملية صحيحة")
        self.show_all_books()

    def delete_book(self):
        code = self.main_window.lineEdit_5.text()
        query = 'DELETE FROM books WHERE code=%s'
        self.main_window.db_ops.execute_query(query, (code,))
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم حذف الكتاب", "عملية صحيحة")
        self.show_all_books()

    def all_book_filter(self):
        pass

    def books_export_report(self):
        pass
