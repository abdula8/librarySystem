class ClientOperations:
    def __init__(self, main_window):
        self.main_window = main_window

    def add_new_client(self):
        client_name = self.main_window.lineEdit_7.text()
        client_email = self.main_window.lineEdit_10.text()
        client_phone = self.main_window.lineEdit_11.text()
        client_national_id = self.main_window.lineEdit_12.text()

        query = '''
            INSERT INTO clients(name, email, phone, national_id)
            VALUES (%s, %s, %s, %s)
        '''
        params = (client_name, client_email, client_phone, client_national_id)
        self.main_window.db_ops.execute_query(query, params)
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم إضافة العميل", "عملية صحيحة")
        self.main_window.lineEdit_7.setText('')
        self.main_window.lineEdit_10.setText('')
        self.main_window.lineEdit_11.setText('')
        self.main_window.lineEdit_12.setText('')

    def edit_client_search(self):
        client_id = self.main_window.lineEdit_13.text()
        query = 'SELECT * FROM clients WHERE id = %s'
        client = self.main_window.db_ops.execute_query(query, (client_id,))

        if client:
            self.main_window.lineEdit_14.setText(client[0][1])
            self.main_window.lineEdit_15.setText(client[0][2])
            self.main_window.lineEdit_16.setText(client[0][3])
            self.main_window.lineEdit_17.setText(client[0][4])

    def edit_client(self):
        client_id = self.main_window.lineEdit_13.text()
        client_name = self.main_window.lineEdit_14.text()
        client_email = self.main_window.lineEdit_15.text()
        client_phone = self.main_window.lineEdit_16.text()
        client_national_id = self.main_window.lineEdit_17.text()

        query = '''
            UPDATE clients SET name=%s, email=%s, phone=%s, national_id=%s WHERE id=%s
        '''
        params = (client_name, client_email, client_phone, client_national_id, client_id)
        self.main_window.db_ops.execute_query(query, params)
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم تعديل بيانات العميل", "عملية صحيحة")

    def delete_client(self):
        client_id = self.main_window.lineEdit_13.text()
        query = 'DELETE FROM clients WHERE id=%s'
        self.main_window.db_ops.execute_query(query, (client_id,))
        self.main_window.db_ops.commit()

        self.main_window.ui_ops.pop_up_message("تم حذف العميل", "عملية صحيحة")

    def client_export_report(self):
        pass
