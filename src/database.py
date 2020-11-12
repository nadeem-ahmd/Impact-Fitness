import csv
import enum
import sqlite3
from tkinter import messagebox as message

from src import settings

try:
    import pymysql
except ImportError:
    print("Failed to import will be unable to use remote database setting.")


class Database:
    """Creates an object defined as a generic Database connection which can read and save data"""

    def __init__(self, File, Table):
        """Establishes core database details"""

        self.File = File
        self.Table = Table

        """Other variables made, assigned to child classes when made"""
        self.Cursor = None
        self.Connection = None

    def Execute(self, Statement):
        """Called to execute a SQL command using statement in parameter"""

        self.Cursor.execute(Statement)

    def Save(self, Data):
        """Called to save data inside a local based database"""

        """Uses database cursor to carry out SQL to delete all items from database table"""
        self.Execute('DELETE FROM ' + self.Table)

        """Uses database cursor to carry out SQL to insert a record for each item in the Data array in the parameter"""
        for Record in Data:
            self.Execute('INSERT INTO ' + self.Table + ' VALUES' + str(tuple(Record.GetAttributes())))

        """Calls function to commit to any updates which have taken place"""
        self.Commit()

    def Read(self):
        """Returns array of data after reading database"""

        """Uses database cursor to carry out SQL to select all items from database table"""
        self.Execute('SELECT * FROM ' + self.Table)

        """Creates array to store data read in local database"""
        self.Data = []

        """Reads through each Record in the result-set and appends the Record to the Data array"""
        for Record in self.Cursor.fetchall():
            self.Data.append(list(Record))
        return self.Data

    def Create(self, Table, Fields):
        """Used to create a new table with attributes specific in parameter"""

        Statement = 'CREATE TABLE ' + Table + '('
        for x in Fields:
            Statement += x[0] + ' ' + x[1] + ', '
        Statement = Statement[:-2] + ')'
        self.Execute(Statement)

    def Insert(self, Data):
        """Used to insert a data item into the database"""

        self.Execute('INSERT INTO ' + self.Table + ' VALUES ' + str(Data.GetAttributes()))
        self.Commit()

    def Delete(self, RowID):
        """Used to delete a data item from the database using RowID in parameter"""

        self.Execute('DELETE FROM ' + self.Table + ' WHERE rowid = ' + RowID)
        self.Commit()

    def Drop(self, Table):
        """Used to drop database table"""

        self.Execute('DROP TABLE ' + Table)

    def Update(self, Table, Field, Value, ID):
        """Used to update a database record using ID parameter"""

        self.Execute('UPDATE ' + Table + ' SET ' + Field + ' = '' + Value + '' WHERE id = ' + ID)

    def SelectAll(self, Table, Order=''):
        """Returns all relevant records from a table using parameters"""

        Statement = 'SELECT * FROM ' + Table
        if Order:
            Statement += ' ORDER BY ' + str(Order)
        return self.Execute(Statement).fetchall()

    def SelectRecord(self, Table, ID, Field='*'):
        """Returns all attributes or specific attributes of a record from a table using the parameters"""

        return self.Execute('SELECT ' + Field + ' FROM ' + Table + ' WHERE id = ' + str(ID)).fetchall()

    def Count(self, Table):
        """Returns the number of records from table specified in parameter"""

        return self.Execute('SELECT count(*) FROM ' + Table)

    def Minimum(self, Table, Attribute):
        """Returns the minimum value from the table in parameter"""

        return self.Execute('SELECT min(' + Attribute + ') FROM ' + Table)

    def Maximum(self, Table, Attribute):
        """Returns the maximum value from the table in parameter"""

        return self.Execute('SELECT max(' + Attribute + ') FROM ' + Table)

    def Average(self, Table, Attribute):
        """Returns the average value from the table in parameter"""

        return self.Execute('SELECT avg(' + Attribute + ') FROM ' + Table)

    def Sum(self, Table, Attribute):
        """Returns the sum value of record attributes from the table in parameter"""

        return self.Execute('SELECT sum(' + Attribute + ') FROM ' + Table)

    def Commit(self):
        """Commits any changes that have been made to the database"""

        self.Connection.commit()


class Local(Database):
    """Creates an object defined as a local database connection which inherits functions from parent class"""

    def __init__(self, File, Table):
        """Establishes the connection to the local database"""

        """Parameters are passed onto the parent Database class"""
        super().__init__(File, Table)

        """Connection is made to local database using file name defined in parameter"""
        self.Connection = sqlite3.connect(self.File)

        """Cursor object is created using Connection object"""
        self.Cursor = self.Connection.cursor()

        """Assigns database type to Local"""
        self.Type = Type.Local

        """Calls function to check the database has all required tables"""
        self.Check()

    def Check(self):
        """Called when database is made, used to check and ensure all required tables exist"""

        """Dictionary stores each table name as well as each attribute and corresponding data type """
        Tables = {
            'Orders': [['OrderID', 'integer'], ['Date', 'string'], ['CustomerID', 'integer']],
            'OrdersItem': [['OrderID', 'integer'], ['ItemID', 'integer'], ['Quantity', 'integer']],
            'Inventory': [['ItemID', 'integer'], ['Brand', 'string'], ['Type', 'string'], ['Name', 'string'],
                          ['Price', 'real'], ['Stock', 'integer']],
            'Customers': [['CustomerID', 'integer'], ['Firstname', 'string'], ['Surname', 'string'],
                          ['Contact', 'string'], ['Address', 'real']]}

        """Iteration through dictionary to create table if it doesn't already exist"""
        for Key in Tables:

            """Builds the final string of attributes for the SQL query"""
            x = ""
            for Attribute in Tables[Key]:
                x = x + Attribute[0] + ' ' + Attribute[1] + ', '
            x = x[:-2]

            """Carries out the SQL query making the table with the key attribute and the built attribute string"""
            self.Execute('CREATE TABLE IF NOT EXISTS ' + Key + ' (' + x + ')')

        """Commits any changes made to the database"""
        self.Commit()


class Remote(Database):
    """Creates an object defined as a remote Database connection which inherits functions from parent class"""

    def __init__(self, Host, User, Password, File, Table):
        """Establishes the connection to the remote database"""

        """Parameters are passed onto the parent Database class"""
        super().__init__(File, Table)

        """Connection is made to remote database using values in parameter, exception handling checking if connection is successful"""
        try:
            self.Connection = pymysql.connect(host=Host, user=User, passwd=Password, db=File)
        except Exception:
            message.showerror('Error', 'Could not connect to remote database, check remote database settings')
            exit()

        """Cursor object is created using Connection object"""
        self.Cursor = self.Connection.cursor()

        """Assigns database type to Remote"""
        self.Type = Type.Remote


class Text(Database):
    """Creates an object defined as a text file Database connection which overrides functions from parent class"""

    def __init__(self, File):
        """Parameters are passed onto the parent Database class"""
        super().__init__(File, None)

        """Assigns database type to Text"""
        self.Type = Type.Text

        """Calls function to check the database has all required tables"""
        self.Check()

    def Check(self):
        """Called when connection is made, used to check and ensure all required tables exist for text database"""

        """List containing all of the tables needed for the system"""
        Tables = ['Orders', 'OrdersItem', 'Inventory', 'Customers']

        """Iteration through each required table"""
        for Table in Tables:

            try:
                """Tries to open the iterated file using the 'r' state, meaning read only, do not delete records"""
                open('../Data/Text/' + Table + '.csv', 'r')
            except IOError:
                """If an error occurs it means the file does not exist", in that case open with 'w' state meaning write, deletes records"""
                open('../Data/Text/' + Table + '.csv', 'w')

    def Save(self, Data):
        """Called to save data inside a text based database"""

        """Connects to and Removes all records from the table due to 'w' parameter"""
        Connection = open('../Data/Text/' + self.File + '.csv', 'w')

        """Creates writer instance for opened text file"""
        Writer = csv.writer(Connection, lineterminator='\n')

        """Writes row inside opened file for each Record in Data parameter by getting attributes"""
        for Record in Data:
            Writer.writerow(list(Record.GetAttributes()))

        """Closing connection when process is complete"""
        Connection.close()

    def Read(self):
        """Returns array of data after reading text based database"""

        """Establishes connection to the local text file"""
        Connection = open('../Data/Text/' + self.File + '.csv', 'r')

        """Creates reader instance for opened text file"""
        Reader = csv.reader(Connection)

        """Creates array to store data read in text file"""
        Data = []

        """Reads through each Record in the reader instance and appends the Record to the Data array"""
        for Record in Reader:
            if Record:
                Data.append(Record)

        """Closing connection when process is complete"""
        Connection.close()
        return Data

    def Insert(self, Data):
        """Used to insert a data item into a text file, overrides parent database class"""

        """Establishes connection to the local text file with append configuration"""
        Connection = open('../Data/Text/' + self.File + '.csv', 'a')

        """Creates writer instance for opened text file"""
        Writer = csv.writer(Connection, lineterminator='\n')

        """Writes row inside opened file for data item in parameter"""
        Writer.writerow(Data.GetAttributes())

        """Closing connection when process is complete"""
        Connection.close()


class Type(enum.Enum):
    """Enum used for different database types"""

    Local = 'Local'
    Remote = 'Remote'
    Text = 'Text'


def Connect(Table):
    """Returns the relevant database connection depending on chosen configuration"""

    DatabaseType = settings.Connect().GetValue('DATABASE', 'TYPE')
    if DatabaseType == Type.Remote.name:
        return Remote(settings.Connect().GetValue('REMOTE', 'HOST'),
                      settings.Connect().GetValue('REMOTE', 'USERNAME'),
                      settings.Connect().GetValue('REMOTE', 'PASSWORD'),
                      'impact', Table)
    elif DatabaseType == Type.Text.name:
        return Text(Table)
    else:
        return Local(settings.Connect().GetValue('LOCAL', 'PATH'), Table)
