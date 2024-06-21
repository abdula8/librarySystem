from peewee import *
import datetime

#db = MySQLDatabase('my_database')
db = MySQLDatabase('library', user='root', password='01099110790aA@',
                     host='localhost', port=3306)
# db = MySQLDatabase('testo', user='root', password='01099110790aA@',
#                      host='localhost', port=3306)


class Category(Model):
    category = CharField(unique=True)
    # parent_category = IntegerField(null=True) ## Recursive relationship

    class Meta:
        database = db


class Publisher(Model):
    name = CharField(unique=True)
    location = CharField(null=True)

    class Meta:
        database = db


class Auther(Model):
    name = CharField(unique=True)
    location = CharField(null=True)

    class Meta:
        database = db


BOOK_STATUS = (
    (1, 'New'),# (DB saved value, user value appearance)
    (2, 'Used'),
    (3, 'Damaged')
    )


class Books(Model):
    # category, publisher, and auther ==> will make error in adding new book because of relations
    # that is occured becuase we created the DB and relations using peewee and not editing it using the peewee.
    # so after creating DB using this code then delete the 3 columns category, auther, and publisher from DB itself manually
    # then create others manually with the same name also.

    title = CharField(unique=True) # unique is used to make the name not to be repeated
    description = TextField(null=True)
    category = ForeignKeyField(Category, backref='category', null=True)
    code = CharField(null=True)
    barcode = CharField()
    # parts 
    part_order = IntegerField(null=True)
    price = DecimalField(null=True)
    publisher = ForeignKeyField(Publisher, backref='publisher', null=True)
    auther = ForeignKeyField(Auther, backref='auther', null=True)           #it should be author but if i change it that will change other code lines
    image = CharField(null=True)
    status = CharField(choices=BOOK_STATUS) # choices
    date = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


class Clients(Model):
    name = CharField()
    mail = CharField(null=True, unique=True)
    phone = CharField(null=True) ## Remember to make a function to check it's only numbers not charcters but you stil can use only '+' char
    date = DateTimeField(default=datetime.datetime.now())
    national_id = CharField(null=True, unique=True)
    
    class Meta:
        database = db


class Employee(Model):
    name = CharField()
    mail = CharField(null=True, unique=True)
    phone = CharField(null=True) ## Remember to make a function to check it's only numbers not charcters but you stil can use only '+' char
    date = DateTimeField(default=datetime.datetime.now())
    national_id = CharField(null=True, unique=True)
    priority = IntegerField(null=True)
    password = CharField()
    branch = CharField()

    class Meta:
        database = db


class Employee_Permission(Model):
    employee_name       = CharField(null=False)
    books_tab           = IntegerField(null=True)
    clients_tab         = IntegerField(null=True)
    dashboard_tab       = IntegerField(null=True)
    history_tab         = IntegerField(null=True)
    reports_tab         = IntegerField(null=True)
    settings_tab        = IntegerField(null=True)
    add_book            = IntegerField(null=True)
    edit_book           = IntegerField(null=True)
    delete_book         = IntegerField(null=True)
    import_book         = IntegerField(null=True)
    export_book         = IntegerField(null=True)
    add_client          = IntegerField(null=True)
    edit_client         = IntegerField(null=True)
    delete_client       = IntegerField(null=True)
    import_client       = IntegerField(null=True)
    export_client       = IntegerField(null=True)
    add_branch          = IntegerField(null=True)
    add_publisher       = IntegerField(null=True)
    add_author          = IntegerField(null=True)
    add_category        = IntegerField(null=True)
    add_employee        = IntegerField(null=True)
    edit_employee       = IntegerField(null=True)
    is_admin            = IntegerField(null=True)

    class Meta:
        database = db



class Branch(Model):
    name = CharField()
    code = CharField(null=True, unique=True)
    location = CharField(null=True)

    class Meta:
        database = db


PROCESS_TRPE = (
    (1, 'Rent'),
    (2, 'Retrieve')
)


class Daily_Movement(Model):
    book = ForeignKeyField(Books, backref='daily_book')
    client = ForeignKeyField(Clients, backref='book_client')
    type_of = CharField(choices=PROCESS_TRPE)
    date = DateTimeField(default=datetime.datetime.now())
    branch = ForeignKeyField(Branch, backref='Daily_branch', null=True)
    Book_from = DateField(null=True)
    Book_to = DateField(null=True)
    employee = ForeignKeyField(Employee, backref='Daily_employee', null=True)

    class Meta:
        database = db


ACTIONS_TYPE = (
    (1, 'Login'),
    (2, 'Update'),
    (3, 'Create'),
    (4, 'Delete'),
)

TABLE_CHOICES = (
    (1, 'Books'),
    (2, 'Clients'),
    (3, 'Employee'),
    (4, 'Category'),
    (5, 'Branch'),
    (6, 'Daily Movement'),
    (7, 'Publisher'),
    (8, 'Auther'),
    # (, )
)


class History(Model):
    # history = 
    employee_id = ForeignKeyField(Employee, backref='History_employee')
    employee_action = CharField(choices=ACTIONS_TYPE) ## will be choices ==>> is used as employee_action not action only
    effected_table = CharField(choices=TABLE_CHOICES) ## choices also
    operation_date = DateTimeField(default=datetime.datetime.now())
    employee_branch = ForeignKeyField(Branch, backref='History_branch')
    data = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Category, Branch, Publisher, Auther, Books, Clients, Employee, Daily_Movement, History, Employee_Permission])




