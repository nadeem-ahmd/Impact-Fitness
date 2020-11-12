from tkinter import *
from tkinter import messagebox as message
from tkinter.ttk import *

from src import database
from src.utils import *


class Customer:
    """Creates an object item to be stored as each customer entity"""

    def __init__(self, CustomerID, Firstname, Surname, Contact, Address):
        """Parameters stored as attributes for each Customer item"""

        self.CustomerID = CustomerID
        self.Firstname = Firstname
        self.Surname = Surname
        self.Contact = Contact
        self.Address = Address

    def GetAttributes(self):
        """Returns the the attributes of the Customer object as a list"""

        return int(self.CustomerID), self.Firstname, self.Surname, self.Contact, self.Address

    def GetID(self):
        """Returns the unique ID of the object"""

        return int(self.CustomerID)


class CustomerManager(Toplevel):
    """Creates an instance of the InventoryManager interface as a subclass of the Tkinter Toplevel widget"""

    def __init__(self, *args, **kwargs):
        """Initialises the different features for the application"""

        """Setting the master class as the argument passed when the class was called, will be Main Menu root instance"""
        self.master = args[0]

        """Parameters are passed onto the Tkinter parent Toplevel class"""
        super().__init__(**kwargs)

        """Sets application title"""
        self.title('Customer Management')

        """Calls class defined functions to connect to database, set up interface and customers"""
        self.LoadDatabase()
        self.LoadInterface()
        self.LoadCustomers(self.Customers)

        """Starts the main loop for the application"""
        self.mainloop()

    def LoadDatabase(self):
        """Called to create connection to Database type specified in the configuration file and reads data"""

        self.Customers = []

        """Creates Customer object for each row found in Database and places object in new Customers array"""
        Records = database.Connect('Customers').Read()
        for Record in Records:
            NewCustomer = Customer(Record[0], Record[1], Record[2], Record[3], Record[4])
            self.Customers.append(NewCustomer)

    def LoadInterface(self):
        """Called to set up the core interface widgets for the application"""

        """Creates and packs the Frame widget onto the root interface using the pack geometry manager"""
        self.TopFrame = Frame(self)
        self.TopFrame.pack(fill=BOTH, padx=10, pady=10)

        """Creates and packs the Frame widget onto the TopFrame frame using the pack geometry manager"""
        self.ButtonWidgets = LabelFrame(self.TopFrame, text='Actions')
        self.ButtonWidgets.pack(side=LEFT)

        """Creates and packs Button widgets onto the Button widget using the grid geometry manager"""
        self.AddButton = Button(self.ButtonWidgets, text='New', command=lambda: NewCustomer(self))  #
        self.AddButton.grid(row=0, column=0)
        self.EditButton = Button(self.ButtonWidgets, text='Edit', command=lambda: EditCustomer(self))
        self.EditButton.grid(row=1, column=0)
        self.DeleteButton = Button(self.ButtonWidgets, text='Delete', command=self.DeleteCustomer)
        self.DeleteButton.grid(row=2, column=0)
        self.RefreshButton = Button(self.ButtonWidgets, text='Refresh', command=self.RefreshCustomers)
        self.RefreshButton.grid(row=3, column=0)

        """Creates and packs the LabelFrame widget onto the TopFrame frame using the pack geometry manager"""
        self.SearchWidgets = LabelFrame(self.TopFrame, text='Search:')
        self.SearchWidgets.pack(side=RIGHT)

        """Specifies the different search options available and creates a variable for the users selection"""
        self.SearchOptions = ('ID', 'Firstname', 'Surname', 'Contact', 'Address')
        self.SearchVariable = StringVar()
        self.SearchVariable.set(self.SearchOptions[0])

        """Creates an OptionMenu widget and packs it onto the SearchWidgets frame using the pack geometry manager"""
        self.SearchOptionsMenu = OptionMenu(self.SearchWidgets, self.SearchVariable, '', *self.SearchOptions)
        self.SearchOptionsMenu.config(width='15')
        self.SearchOptionsMenu.grid(row=0, column=0)

        """Creates an Entry widget, packs it onto the SearchWidgets frame, then binds a keyboard action to a function"""
        self.SearchEntry = Entry(self.SearchWidgets)
        self.SearchEntry.grid(row=1, column=0)
        self.SearchEntry.bind('<KeyRelease>', self.Search)

        """Creates and packs the Frame widget onto the root interface using the pack geometry manager, below TopFrame"""
        self.BottomFrame = LabelFrame(self, text='Customers')
        self.BottomFrame.pack(fill=BOTH, expand=TRUE)

        """Creates and packs Treeview widget onto the BottomFrame frame, binds functions and hides headings"""
        self.CustomerTreeview = Treeview(self.BottomFrame, height=20)
        self.CustomerTreeview.pack(side=LEFT, expand=TRUE, fill=BOTH)
        self.CustomerTreeview.bind('<Button-1>', self.ClickTree)
        self.CustomerTreeview['show'] = 'headings'

        """Creates Scrollbar widget and packs it beside Treeview on the BottomFrame and assigns scroll command"""
        self.CustomerTreeviewScrollbar = Scrollbar(self.BottomFrame, command=self.CustomerTreeview.yview)
        self.CustomerTreeviewScrollbar.pack(side=RIGHT, fill=Y)
        self.CustomerTreeview.config(yscrollcommand=self.CustomerTreeviewScrollbar.set)

        """Specifies the Attributes and Headers for each Treeview column/row"""
        self.Attributes = ('id', 'firstname', 'surname', 'contact', 'address')
        self.Headers = ('ID', 'Firstname', 'Surname', 'Contact', 'Address')
        self.CustomerTreeview['columns'] = self.Attributes

        """Creates each column in Treeview for each item in Headers array, specifying title, anchor and length"""
        for Header in self.Headers:
            self.CustomerTreeview.heading(self.Attributes[self.Headers.index(Header)], text=Header, anchor=W)
            self.CustomerTreeview.column(self.Attributes[self.Headers.index(Header)], width=160, minwidth=160)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadCustomers(self, Data):
        """Called to load the Treeview widget with the data in list specified in the parameter"""

        """Calls function to remote all of the items already existing in the Treeview widget"""
        self.ResetCustomers()

        """Inserts a new item at index i with values specified as long as there is an item in the Data parameter"""
        if Data:
            i = 0
            for Record in Data:
                self.CustomerTreeview.insert('', END, text=i, values=(Record.GetAttributes()))
                i += 1

            """Sets the current selected item as the first value which will also trigger the TreeviewSelect function"""
            self.CustomerTreeview.selection_set(self.CustomerTreeview.get_children()[0])

    def SaveCustomers(self, Data):
        """Called to save the data stored in the class defined Data list in the database"""

        database.Connect('Customers').Save(Data)

    def ResetCustomers(self):
        """Called to remove all the items already stored inside the Treeview widget"""

        self.CustomerTreeChildren = self.CustomerTreeview.get_children()
        for Child in self.CustomerTreeChildren:
            self.CustomerTreeview.delete(Child)

    def GetSelectedCustomer(self):
        """Returns the values for the item dictionary which is currently selected in the Treeview"""

        self.Selected = self.CustomerTreeview.selection()
        for Customer in self.Selected:
            self.SelectedIndex = self.CustomerTreeview.item(Customer)
            self.SelectedRecord = self.SelectedIndex['values']
        return self.SelectedRecord

    def DeleteCustomer(self):
        """Called when the Delete button is pressed, used to remove the selected customer from the customer list"""

        """Prompts the user for removal confirmation and will continue if the user selects YES"""
        Confirm = message.askquestion('Remove', 'Remove customer from list?', icon='warning', parent=self)
        if Confirm == message.YES:

            """Definite iteration through Customer array looking for selected customer"""
            for DataItem in self.Customers:
                if int(DataItem.CustomerID) == int(self.GetSelectedCustomer()[0]):
                    """Removes item from Data list as well as Treeview when match is found"""
                    self.Customers.remove(DataItem)
                    self.CustomerTreeview.delete(self.Selected[0])

            """Calls the class defined method to save Customers information now that an item has been removed"""
            self.SaveCustomers(self.Customers)

            """As long as there is at least one result, set the first option in the Treeview widget"""
            if self.Customers:
                self.CustomerTreeview.selection_set(self.CustomerTreeview.get_children()[0])

    def Search(self, Event):
        """Called when the SearchEntry is edited using the <KeyRelease> binding"""

        """Gets the user input of the SearchEntry widget and the SearchVariable (OptionsMenu choice)"""
        self.Query = self.SearchEntry.get()
        self.Attribute = self.SearchVariable.get()

        """Creates a new array to store the results of the search attempt"""
        self.Results = []

        """Definite iteration checking each item in the Data array with input specified in the Entry and OptionsMenu"""
        for DataItem in self.Customers:
            if str(self.Query).lower() in \
                    str(DataItem.GetAttributes()[(self.SearchOptions.index(self.Attribute))]).lower():
                """Append the Item object to the results array if the condition is met"""
                self.Results.append(DataItem)

        """Calls the function to load the Treeview widget with the Results list"""
        self.LoadCustomers(self.Results)

        """As long as there is at least one result, set the first option in the Treeview widget"""
        if self.Results:
            self.CustomerTreeview.selection_set(self.CustomerTreeview.get_children()[0])

    def ClickTree(self, Event):
        """Called to change the Treeview to a different sort type, activated by clicking header using Event parameter"""

        """Function is called for every click on Treeview so checks whether click region is header"""
        self.ClickedRegion = self.CustomerTreeview.identify('region', Event.x, Event.y)
        if self.ClickedRegion == 'heading':
            """Calls function to load the customers with a sorted list"""
            self.LoadCustomers(SortTree(Event, self.CustomerTreeview, self.Customers))

    def RefreshCustomers(self):
        """Called when the Refresh button is pressed, used to save and refresh the customers"""

        self.SaveCustomers(self.Customers)
        self.LoadCustomers(self.Customers)


class NewCustomer(Toplevel):
    """Creates an instance of the New interface as a subclass of the Tkinter TopLevel widget with Inventory as root"""

    def __init__(self, *args, **kwargs):
        """Parameters are passed onto the Tkinter parent Frame class"""
        super().__init__(**kwargs)

        """Setting the master class as the argument passed when the class was called, will be Inventory"""
        self.master = args[0]

        """Sets the window title of the new TopLevel instance"""
        self.title('New Customer')

        """Calls class defined functions to set up interface"""
        self.LoadInterface()

    def LoadInterface(self):
        """Creates and packs the MainFrame widget onto the root interface using the pack geometry manager"""
        self.MainFrame = Frame(self)
        self.MainFrame.pack()

        """Creates and packs the Label widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDLabel = Label(self.MainFrame, text='ID:')
        self.IDLabel.grid(row=0, column=0, sticky=W, padx=10)
        self.FirstnameLabel = Label(self.MainFrame, text='Firstname:')
        self.FirstnameLabel.grid(row=1, column=0, sticky=W, padx=10)
        self.SurnameLabel = Label(self.MainFrame, text='Surname:')
        self.SurnameLabel.grid(row=2, column=0, sticky=W, padx=10)
        self.ContactLabel = Label(self.MainFrame, text='Contact:')
        self.ContactLabel.grid(row=3, column=0, sticky=W, padx=10)
        self.AddressLabel = Label(self.MainFrame, text='Address:')
        self.AddressLabel.grid(row=4, column=0, sticky=W, padx=10)

        """Creates and packs the Entry widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDEntry = Entry(self.MainFrame, width=25)
        self.IDEntry.grid(row=0, column=1, padx=10, pady=5)
        self.FirstnameEntry = Entry(self.MainFrame, width=25)
        self.FirstnameEntry.grid(row=1, column=1, padx=10, pady=5)
        self.SurnameEntry = Entry(self.MainFrame, width=25)
        self.SurnameEntry.grid(row=2, column=1, padx=10, pady=5)
        self.ContactEntry = Entry(self.MainFrame, width=25)
        self.ContactEntry.grid(row=3, column=1, padx=10, pady=5)
        self.AddressEntry = Entry(self.MainFrame, width=25)
        self.AddressEntry.grid(row=4, column=1, padx=10, pady=5)

        """Creates a new button and packs it onto the MainFrame frame using the grid geometry manager """
        self.FinishedButton = Button(self.MainFrame, text='Finished', command=self.Finished)
        self.FinishedButton.grid(row=6, columnspan=2, pady=5)

        """As the ID entry should be unique, it is auto-generated based on the customers existing in the data"""
        self.IDEntry.insert(0, self.GenerateID())

        """Sets entry in first index to disabled state after it's loaded so it cannot be edited by the user"""
        self.IDEntry.configure(state=DISABLED)

        """Binds the return key to call the Finished function"""
        self.bind('<Return>', self.Finished)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def GenerateID(self):
        """Returns the unique ID the new item should be stored as, checks through inventory"""

        """Definite iteration through Data list checking if generated ID already exists"""
        GeneratedID = 1
        for DataItem in self.master.Customers:

            """If generated ID does not exist for this customer, it is available so return the generated number"""
            if int(DataItem.CustomerID) is not int(GeneratedID):
                return GeneratedID

            """Else add one to generated ID and reiterate"""
            GeneratedID += 1

        """Final number should be available as it will be the final generated ID plus one"""
        return GeneratedID

    def ValidFields(self):
        """Returns whether it is possible to create valid customer object"""

        """Attempts to create Customer object using provided input, returns true if possible or error if not"""
        try:
            Customer(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4])
            return True
        except ValueError as E:
            message.showerror('Error', 'Check fields for error: ' + str(E), parent=self)
            return False

    def Finished(self):
        """Called when the user presses the Finished button, used to save the new Customer"""

        """Creates a new list and places all the entries previously specified for easy usage"""
        self.Entries = [self.IDEntry, self.FirstnameEntry, self.SurnameEntry, self.ContactEntry, self.AddressEntry]

        """Creates a new list and appends all the values from all Entry widgets stored in the Entries list"""
        self.Input = []
        for Entry in self.Entries:
            self.Input.append(Entry.get())

        """If input entries are valid, continue on to add the customer"""
        if self.ValidFields():
            """Creates a new Item object using the all indexes specified in the Inputs list"""
            self.NewCustomer = Customer(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4])

            """Adds customer into data using built in insert function, inserts at the first location relevant to ID"""
            self.master.Customers.insert(int(self.Input[0]) - 1, self.NewCustomer)

            """Calls the class defined method in Customers to save customer data now that a customer has been added"""
            self.master.SaveCustomers(self.master.Customers)

            """Calls the class defined method in Customer to update the Treeview with the new customer data"""
            self.master.LoadCustomers(self.master.Customers)

            """Built-in defined method used to destroy the New interface"""
            self.destroy()


class EditCustomer(Toplevel):
    """Creates an instance of the New interface as a subclass of the Tkinter TopLevel widget with Inventory as root"""

    def __init__(self, *args, **kwargs):
        """Parameters are passed onto the Tkinter parent Frame class"""
        super().__init__(**kwargs)

        """Setting the master class as the argument passed when the class was called, will be Inventory"""
        self.master = args[0]

        """Sets the window title of the new TopLevel instance"""
        self.title('Edit Customer')

        """Calls class defined functions to set up interface and load customer data"""
        self.LoadInterface()
        self.LoadCustomer()

    def LoadInterface(self):
        """Creates and packs the MainFrame widget onto the root interface using the pack geometry manager"""
        self.MainFrame = Frame(self)
        self.MainFrame.pack()

        """Creates and packs the Label widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDLabel = Label(self.MainFrame, text='ID:')
        self.IDLabel.grid(row=0, column=0, sticky=W, padx=10)
        self.FirstnameLabel = Label(self.MainFrame, text='Firstname:')
        self.FirstnameLabel.grid(row=1, column=0, sticky=W, padx=10)
        self.SurnameLabel = Label(self.MainFrame, text='Surname:')
        self.SurnameLabel.grid(row=2, column=0, sticky=W, padx=10)
        self.ContactLabel = Label(self.MainFrame, text='Contact:')
        self.ContactLabel.grid(row=3, column=0, sticky=W, padx=10)
        self.AddressLabel = Label(self.MainFrame, text='Address:')
        self.AddressLabel.grid(row=4, column=0, sticky=W, padx=10)

        """Creates and packs the Entry widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDEntry = Entry(self.MainFrame, width=25)
        self.IDEntry.grid(row=0, column=1, padx=10, pady=5)
        self.FirstnameEntry = Entry(self.MainFrame, width=25)
        self.FirstnameEntry.grid(row=1, column=1, padx=10, pady=5)
        self.SurnameEntry = Entry(self.MainFrame, width=25)
        self.SurnameEntry.grid(row=2, column=1, padx=10, pady=5)
        self.ContactEntry = Entry(self.MainFrame, width=25)
        self.ContactEntry.grid(row=3, column=1, padx=10, pady=5)
        self.AddressEntry = Entry(self.MainFrame, width=25)
        self.AddressEntry.grid(row=4, column=1, padx=10, pady=5)

        """Creates a new button and packs it onto the MainFrame frame using the grid geometry manager """
        self.FinishedButton = Button(self.MainFrame, text='Finished', command=self.Finished)
        self.FinishedButton.grid(row=6, columnspan=2, pady=5)

        """Binds the return key to call the Finished function"""
        self.bind('<Return>', self.Finished)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadCustomer(self):
        """Called to fill entries with selected customer information for easy editing"""

        self.CustomerRecords = self.master.GetSelectedCustomer()
        self.Entries = [self.IDEntry, self.FirstnameEntry, self.SurnameEntry, self.ContactEntry, self.AddressEntry]
        for Entry in self.Entries:
            Entry.insert(0, self.CustomerRecords[self.Entries.index(Entry)])

        """Disables ID entry so user cannot edit unique field"""
        self.IDEntry.configure(state=DISABLED)

    def ValidFields(self):
        """Returns whether it is possible to create valid Customer object"""

        """Attempts to create Customer object using provided input, returns true if possible or error if not"""
        try:
            Customer(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4])
            return True
        except ValueError as E:
            message.showerror('Error', 'Check fields for error: ' + str(E), parent=self)
            return False

    def Finished(self, *Event):
        """Called when the user presses the Finished button, used to save the new Customer"""

        """Creates a new list and appends all the values from all Entry widgets stored in the Entries list"""
        self.Input = []
        for Entry in self.Entries:
            self.Input.append(Entry.get())

        """If input entries are valid, continue on to add the Customer"""
        if self.ValidFields():
            """Creates a new Customer object using the all indexes specified in the Inputs list"""
            self.NewCustomer = Customer(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4])

            """Replaces existing customer object with new customer object"""
            for CustomerRecord in self.master.Customers:
                if int(CustomerRecord.CustomerID) == int(self.IDEntry.get()):
                    self.master.Customers[self.master.Customers.index(CustomerRecord)] = self.NewCustomer

            """Calls the class defined method to save customer data now that a customer has been added"""
            self.master.SaveCustomers(self.master.Customers)
            self.master.LoadCustomers(self.master.Customers)

            """Built-in defined method used to destroy the New interface"""
            self.destroy()
