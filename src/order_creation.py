import datetime
from tkinter import *
from tkinter import messagebox as message
from tkinter.ttk import *

from src import database
from src.utils import *


class Order(list):
    """Creates an object to be stored as each order, acts as a list with main attributes in parameters"""

    def __init__(self, OrderID=None, Date=None, CustomerID=None):
        """Super method is called for the parent class"""
        super().__init__()

        """Parameters stored as attributes for each Order item"""
        self.OrderID = OrderID
        self.Date = Date
        self.CustomerID = CustomerID

    def GetAttributes(self):
        """Returns the attributes of the Order object as a list"""

        return int(self.OrderID), self.Date, int(self.CustomerID)

    def Completed(self):
        """Returns whether all of the attributes are fulfilled"""

        if self.OrderID and self.Date and self.CustomerID and self:
            return True
        return False


class OrdersItem:
    """Creates an object item to be stored in order objects"""

    def __init__(self, OrderID, ItemID, Quantity):
        """Parameters stored as attributes for each OrderItem item"""

        self.OrderID = OrderID
        self.ItemID = ItemID
        self.Quantity = Quantity

    def GetAttributes(self):
        """Returns the attributes of the OrderItem object as a list"""

        return int(self.OrderID), int(self.ItemID), int(self.Quantity)


class Item:
    """Creates an object to be stored in the Inventory array"""

    def __init__(self, ItemID, Brand, Type, Name, Price, Stock):
        self.ItemID = int(ItemID)
        self.Brand = str(Brand)
        self.Type = str(Type)
        self.Name = str(Name)
        self.Price = float(Price)
        self.Stock = int(Stock)

    def GetAttributes(self):
        """Returns the the attributes of the Item object as a list"""

        return int(self.ItemID), self.Brand, self.Type, self.Name, float('{0:.2f}'.format(self.Price)), int(
            self.Stock)


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


class OrderCreation(Toplevel):
    """Creates an instance of the OrderCreation interface as a subclass of the Tkinter Toplevel widget"""

    def __init__(self, *args, **kwargs):
        """Initialises the different features for the application"""

        """Setting the master class as the argument passed when the class was called, will be Root in main class"""
        self.master = args[0]

        """Parameters are passed onto the Tkinter parent Toplevel class"""
        super().__init__(**kwargs)

        """Sets application title"""
        self.title('Order Creation')

        """Calls class defined functions to connect to database, set up interface and order  items"""
        self.LoadDatabase()
        self.LoadInterface()
        self.LoadOrder()

        """Starts the main loop for the application"""
        self.mainloop()

    def LoadDatabase(self):
        """Called to create connection to Database type specified in the configuration file and reads data"""

        self.Inventory = []

        """Creates Item object for each row found in Database and places object in new Inventory array"""
        Records = database.Connect('Inventory').Read()
        for Record in Records:
            self.Inventory.append(Item(Record[0], Record[1], Record[2], Record[3], Record[4], Record[5]))

    def LoadInterface(self):
        """Called to set up the core interface widgets for the application"""

        """Creates and packs the Frame widget onto the root interface using the pack geometry manager"""
        self.OrderFrame = Frame(self)
        self.OrderFrame.pack(fill=BOTH, side=LEFT, padx=15, pady=15)

        """Creates and packs the LabelFrame widget onto the OrderFrame frame using the pack geometry manager"""
        self.OrderButtons = LabelFrame(self.OrderFrame, text='Order Actions')
        self.OrderButtons.pack(fill=BOTH)

        """Creates and packs various buttons onto OrderButtons frame and assigns commands for each"""
        self.AddButton = Button(self.OrderButtons, text='Add', width=15, command=lambda: InventorySelection(self))
        self.AddButton.pack(pady=1)
        self.RemoveButton = Button(self.OrderButtons, text='Remove', width=15, command=self.RemoveFromOrder)
        self.RemoveButton.pack(pady=1)
        self.FinishButton = Button(self.OrderButtons, text='Finish', width=15, command=self.Finished)
        self.FinishButton.pack(pady=1)

        """Creates and packs the LabelFrame widget onto the OrderFrame frame using the pack geometry manager"""
        self.OrderDetails = LabelFrame(self.OrderFrame, text='Order Details')
        self.OrderDetails.pack(fill=BOTH, pady=15)

        """Creates and packs the various Label, Entry and Buttons for the order details panel, assigns commands"""
        self.IDLabel = Label(self.OrderDetails, text='Order ID:')
        self.IDLabel.pack(anchor=W, pady=1)
        self.IDEntry = Entry(self.OrderDetails, width=16)
        self.IDEntry.pack(anchor=W)
        self.DateLabel = Label(self.OrderDetails, text='Date:')
        self.DateLabel.pack(anchor=W, pady=1)
        self.DateEntry = Entry(self.OrderDetails, width=16)
        self.DateEntry.pack(anchor=W)
        self.CustomerLabel = Label(self.OrderDetails, text='Customer:')
        self.CustomerLabel.pack(anchor=W, pady=1)
        self.CustomerButton = Button(self.OrderDetails, text='Select', width=15,
                                     command=lambda: CustomerSelection(self))
        self.CustomerButton.pack(anchor=W)
        self.NetLabel = Label(self.OrderDetails, text='Order Net:')
        self.NetLabel.pack(anchor=W)
        self.NetEntry = Entry(self.OrderDetails, width=16)
        self.NetEntry.pack(anchor=W)

        """Creates and packs the Frame widget onto the root interface using the pack geometry manager"""
        self.OrdersItemFrame = Frame(self)
        self.OrdersItemFrame.pack(fill=BOTH, expand=TRUE, side=LEFT, padx=5, pady=5)

        """Creates and packs Treeview widget onto the OrdersItemFrame frame and hides headings"""
        self.OrderTree = Treeview(self.OrdersItemFrame, height=25)
        self.OrderTree.pack(side=LEFT, expand=TRUE, fill=BOTH)
        self.OrderTree['show'] = 'headings'

        """Creates Scrollbar widget and packs it beside Treeview on the OrdersItemFrame and assigns scroll command"""
        self.OrderTreeScrollbar = Scrollbar(self.OrdersItemFrame, command=self.OrderTree.yview)
        self.OrderTreeScrollbar.pack(side=RIGHT, fill=Y)
        self.OrderTree.config(yscrollcommand=self.OrderTreeScrollbar.set)

        """Specifies the Attributes and Headers for each Treeview column/row"""
        self.OrderAttributes = ('id', 'name', 'price', 'quantity', 'net')
        self.OrderHeaders = ('ID', 'Name', 'Price', 'Quantity', 'Net')
        self.OrderTree['columns'] = self.OrderAttributes

        """Creates each column in Treeview for each item in Headers array, specifying title, anchor and length"""
        for Header in self.OrderHeaders:
            self.OrderTree.heading(self.OrderAttributes[self.OrderHeaders.index(Header)], text=Header, anchor=W)
            self.OrderTree.column(self.OrderAttributes[self.OrderHeaders.index(Header)], width=135, minwidth=135)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadOrder(self):
        """Called to create first instance object of an Order"""

        """Creates initial object calling functions to generate a unique ID and the current date in the parameters"""
        self.Order = Order(self.GenerateID(), self.GenerateDate())

        """Function called to set up the order details on the left panel"""
        self.LoadOrderDetails()

    def LoadOrderDetails(self):
        """Called to populate the Entry widgets with the different order attributes"""

        self.Attributes = [self.Order.OrderID, self.Order.Date, 0]
        self.Entries = [self.IDEntry, self.DateEntry, self.NetEntry]
        for Entry in self.Entries:
            Entry.delete(0, END)
            Entry.insert(END, self.Attributes[self.Entries.index(Entry)])

    def GenerateID(self):
        """Returns the unique ID the new order should be stored as, checks through existing orders"""

        Records = database.Connect('Orders').Read()

        """Definite iteration through Records list checking if generated ID already exists"""
        GeneratedID = 1
        for DataItem in Records:

            """If generated ID does not exist for this item, it is available so return the generated number"""
            if int(DataItem[0]) is not GeneratedID:
                return GeneratedID

            """Else add one to generated ID and reiterate"""
            GeneratedID += 1

        """Final number should be available as it will be the final generated ID plus one"""
        return GeneratedID

    def GenerateDate(self):
        """Returns the current date in the format DD/MM/YYYY"""

        Date = datetime.datetime.now()
        return str(Date.day) + '/' + str(Date.month) + '/' + str(Date.year)

    def LoadOrderTree(self, Data):
        """Called to load the Treeview widget with the data in list specified in the parameter"""

        """Calls function to remote all of the items already existing in the Treeview widget"""
        self.ResetOrder()

        """Inserts a new item at index i with values specified by gathering item details using GetItemDetails"""
        i = 0
        for Record in Data:
            Values = self.GetItemDetails(Record)
            self.OrderTree.insert('', END, text=i, values=(Values[0], Values[1], Values[2], Record.Quantity,
                                                           float('{0:.2f}'.format(Values[2] * Record.Quantity))))
            i += 1

        """Calls the function to update the net order value"""
        self.UpdateOrderNet()

    def ResetOrder(self):
        """Called to remove all the items already stored inside the Treeview widget"""

        self.OrderTreeviewChildren = self.OrderTree.get_children()
        for Child in self.OrderTreeviewChildren:
            self.OrderTree.delete(Child)

    def GetItemDetails(self, OrderItem):
        """Returns item attributes for the record stored in the inventory with the ID in the parameter OrderItem"""

        for Item in self.Inventory:
            if int(OrderItem.ItemID) == int(Item.ItemID):
                return int(Item.ItemID), str(Item.Name), float(Item.Price)

    def UpdateOrderNet(self):
        """Called to gather the price amount of each sub order item and insert it into the NetEntry widget"""

        Net = 0
        for i in self.OrderTree.get_children():
            Values = self.OrderTree.item(i)['values']

            """Converts the value into a float, adds it to the existing net and rounds it to 2 d.p"""
            Net = float('{0:.2f}'.format(Net + float(Values[4])))

        """Deletes any existing contents in the Entry box then inserts the new Net"""
        self.NetEntry.delete(0, END)
        self.NetEntry.insert(END, Net)

    def RemoveFromOrder(self):
        """Used to remove an OrderItem from the Order"""

        Attributes = self.GetSelectedItemAttributes()

        """Selection checking whether an item is selected, if not, present error message"""
        if self.OrderTree.selection():

            """Prompts the user for removal confirmation and will continue if the user selects YES"""
            Confirm = message.askquestion('Remove', 'Remove item from order?', icon='warning', parent=self)
            if Confirm == message.YES:

                """Iterates through Order and removes relevant OrderItem when found, as well as from Treeview"""
                for OrderItem in self.Order:
                    if OrderItem.ItemID == Attributes[0]:
                        self.Order.remove(OrderItem)
                        self.OrderTree.delete(self.Selection[0])

                        """Adds back the stock from the inventory item from when it was added to the order"""
                        for Item in self.Inventory:
                            if Item.ItemID == Attributes[0]:
                                Item.Stock += Attributes[3]

            """Calls the function to update the net order value"""
            self.UpdateOrderNet()
        else:
            message.showerror('Error', 'No item was selected, try again', parent=self)

    def GetSelectedItemAttributes(self):
        """Returns the tree values of the currency selected order"""

        self.Selection = self.OrderTree.selection()
        for Selected in self.Selection:
            return self.OrderTree.item(Selected)['values']

    def Finished(self):
        """Binded to the FinishButton widget, can be called when the user wishes to complete the order"""

        """Checks whether all of the necessary requirements have been met for the order, if not, send error message"""
        if self.Order.Completed():

            """Inserts the new Order into the Orders table"""
            database.Connect('Orders').Insert(self.Order)

            """Inserts a new OrdersItem record into the database for each OrderItem in the Order array"""
            for OrdersItem in self.Order:
                database.Connect('OrdersItem').Insert(OrdersItem)

            """Updates the inventory table as the stock levels have been adjusted after the order"""
            database.Connect('Inventory').Save(self.Inventory)

            """Once the order has been saved, terminate the application"""
            self.destroy()
        else:
            message.showerror('Error', 'Order is not complete', parent=self)


class InventorySelection(Toplevel):
    """Creates an instance of the InventorySelection interface as a subclass of TopLevel with OrderCreation as root"""

    def __init__(self, *args, **kwargs):
        """Parameters are passed onto the Tkinter parent Frame class"""
        super().__init__(**kwargs)

        """Argument index 0 is assigned a variable and is used to reference master class (OrderCreation)"""
        self.OrderCreation = args[0]

        """Sets the window title of the new TopLevel instance"""
        self.title('Item Selection')

        """Calls class defined functions to set up interface and inventory with data from the master class"""
        self.LoadInterface()
        self.LoadInventory(self.OrderCreation.Inventory)

    def LoadInterface(self):
        """Creates and packs the InventoryFrame widget onto the root interface using the pack geometry manager"""
        self.InventoryFrame = LabelFrame(self, text='Inventory')
        self.InventoryFrame.pack(fill=BOTH, expand=TRUE, side=RIGHT)

        """Creates and packs the LabelFrame widget onto the InventoryFrame using the pack geometry manager"""
        self.SearchWidgets = LabelFrame(self.InventoryFrame, text='Search:')
        self.SearchWidgets.pack(side=TOP, pady=5)

        """Specifies the different search options available and creates a variable for the users selection"""
        self.SearchOptions = ('ID', 'Brand', 'Type', 'Name', 'Price', 'Stock')
        self.SearchVariable = StringVar()
        self.SearchVariable.set(self.SearchOptions[3])

        """Creates an OptionMenu widget and packs it onto the SearchWidgets frame using the pack geometry manager"""
        self.SearchOptionsMenu = OptionMenu(self.SearchWidgets, self.SearchVariable, '', *self.SearchOptions)
        self.SearchOptionsMenu.config(width='15')
        self.SearchOptionsMenu.pack(anchor=W)

        """Creates an Entry widget, packs it onto the SearchWidgets frame, then binds a keyboard action to a function"""
        self.SearchEntry = Entry(self.SearchWidgets)
        self.SearchEntry.pack(anchor=CENTER)
        self.SearchEntry.bind('<KeyRelease>', self.Search)

        """Focuses the user input on the Search entry for quick usability"""
        self.SearchEntry.focus_force()

        """Creates and packs Treeview widget onto the InventoryFrame frame, binds functions and hides headings"""
        self.InventoryTree = Treeview(self.InventoryFrame, height=20)
        self.InventoryTree.pack(side=LEFT, expand=TRUE, fill=BOTH)
        self.InventoryTree.bind('<<TreeviewSelect>>', self.QuantitySelection)
        self.InventoryTree['show'] = 'headings'

        """Creates Scrollbar widget and packs it beside Treeview on the InventoryFrame and assigns scroll command"""
        self.InventoryTreeScrollbar = Scrollbar(self.InventoryFrame, command=self.InventoryTree.yview)
        self.InventoryTreeScrollbar.pack(side=RIGHT, fill=Y)
        self.InventoryTree.config(yscrollcommand=self.InventoryTreeScrollbar.set)

        """Specifies the Attributes and Headers for each Treeview column/row"""
        self.InventoryAttributes = ('id', 'brand', 'type', 'name', 'price', 'Stock')
        self.InventoryHeaders = ('ID', 'Brand', 'Type', 'Name', 'Price', 'Stock')
        self.InventoryTree['columns'] = self.InventoryAttributes

        """Creates each column in Treeview for each item in Headers array, specifying title, anchor and length"""
        for Header in self.InventoryHeaders:
            self.InventoryTree.heading(self.InventoryAttributes[self.InventoryHeaders.index(Header)], text=Header,
                                       anchor=W)
            self.InventoryTree.column(self.InventoryAttributes[self.InventoryHeaders.index(Header)], width=115,
                                      minwidth=115)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadInventory(self, Data):
        """Called to load the Treeview widget with the data in list specified in the parameter"""

        """Calls function to remote all of the items already existing in the Treeview widget"""
        self.ResetInventory()

        """Inserts a new item with values specified using record attributes"""
        for Record in Data:
            self.InventoryTree.insert('', END, text=Data.index(Record), values=(Record.GetAttributes()))

    def ResetInventory(self):
        """Called to remove all the items already stored inside the Treeview widget"""

        self.ProductTreeviewChildren = self.InventoryTree.get_children()
        for Child in self.ProductTreeviewChildren:
            self.InventoryTree.delete(Child)

    def Search(self, Event):
        """Called when the SearchEntry is edited using the <KeyRelease> binding"""

        """Gets the user input of the SearchEntry widget and the SearchVariable (OptionsMenu choice)"""
        self.Query = self.SearchEntry.get()
        self.Attribute = self.SearchVariable.get()

        """Creates a new array to store the results of the search attempt"""
        self.Results = []

        """Definite iteration checking each item in Inventory from master class using specified inputs"""
        for DataItem in self.OrderCreation.Inventory:
            if str(self.Query).lower() in \
                    str(DataItem.GetAttributes()[(self.SearchOptions.index(self.Attribute))]).lower():
                """Append the Item object to the results array if the condition is met"""
                self.Results.append(DataItem)

        """Calls the function to load the Treeview widget with the Results list"""
        self.LoadInventory(self.Results)

    def GetSelectedItem(self):
        """Returns the values for the item dictionary which is currently selected in the Treeview"""

        for Selection in self.InventoryTree.selection():
            Selected = self.InventoryTree.item(Selection)
            return Selected['values']

    def QuantitySelection(self, Event):
        """Called when the Treeview item is selected using the <<TreeviewSelect>> binding, gives input options"""

        QuantitySelection(self, self.OrderCreation)


class QuantitySelection(Toplevel):
    """Creates an instance of the QuantitySelection interface as subclass of TopLevel with OrderCreation as root"""

    def __init__(self, *args, **kwargs):
        """Parameters are passed onto the Tkinter parent Frame class"""
        super().__init__(**kwargs)

        """Setting the master class as the argument passed when the class was called, will be InventorySelection"""
        self.InventorySelection = args[0]

        """Setting the master class of the master class, which is the main application OrderCreation    """
        self.OrderCreation = args[1]

        """Sets the window title of the new TopLevel instance"""
        self.title('Add Item')

        """Calls class defined functions to set up interface and entry inputs"""
        self.LoadInterface()
        self.LoadInput()

    def LoadInterface(self):
        """Creates and packs the MainFrame widget onto the root interface using the pack geometry manager"""
        self.MainFrame = Frame(self)
        self.MainFrame.pack()

        """Creates and packs the Label widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDLabel = Label(self.MainFrame, text='ID:')
        self.IDLabel.grid(row=0, column=0, sticky=W, padx=10)
        self.NameLabel = Label(self.MainFrame, text='Name:')
        self.NameLabel.grid(row=1, column=0, sticky=W, padx=10)
        self.PriceLabel = Label(self.MainFrame, text='Price:')
        self.PriceLabel.grid(row=2, column=0, sticky=W, padx=10)
        self.StockLabel = Label(self.MainFrame, text='Stock:')
        self.StockLabel.grid(row=3, column=0, sticky=W, padx=10)
        self.QuantityLabel = Label(self.MainFrame, text='Quantity:')
        self.QuantityLabel.grid(row=4, column=0, sticky=W, padx=10)

        """Creates and packs the Entry widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDEntry = Entry(self.MainFrame, width=25)
        self.IDEntry.grid(row=0, column=1, padx=10, pady=5)
        self.NameEntry = Entry(self.MainFrame, width=25)
        self.NameEntry.grid(row=1, column=1, padx=10, pady=5)
        self.PriceEntry = Entry(self.MainFrame, width=25)
        self.PriceEntry.grid(row=2, column=1, padx=10, pady=5)
        self.StockEntry = Entry(self.MainFrame, width=25)
        self.StockEntry.grid(row=3, column=1, padx=10, pady=5)
        self.QuantityEntry = Entry(self.MainFrame, width=25)
        self.QuantityEntry.grid(row=4, column=1, padx=10, pady=5)

        """Creates a new button and packs it onto the MainFrame frame using the grid geometry manager """
        self.FinishedButton = Button(self.MainFrame, text='Finished', command=self.Finished)
        self.FinishedButton.grid(row=6, columnspan=2, pady=5)

        """Binds the return key to call the Finished function"""
        self.bind('<Return>', self.Finished)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadInput(self):
        """Called to populate existing entries with relevant data, such as the ID, name"""

        """Gathers the values for the selected inventory item"""
        self.SelectedItem = self.InventorySelection.GetSelectedItem()

        """Sets each entry to the relevant value using both arrays"""
        self.Values = [self.SelectedItem[0], self.SelectedItem[3], self.SelectedItem[4], self.SelectedItem[5]]
        self.Entries = [self.IDEntry, self.NameEntry, self.PriceEntry, self.StockEntry]
        for Entry in self.Entries:
            """Deletes any existing data stored in entry"""
            Entry.delete(0, END)

            """Inserts the values relevant for the entry"""
            Entry.insert(END, self.Values[self.Entries.index(Entry)])

            """Sets the entry as disabled so the user cannot edit values"""
            Entry.configure(state=DISABLED)

        """Focuses the user input on the Quantity entry for quick usability with the return key"""
        self.QuantityEntry.focus_force()

    def ValidField(self):
        """Checks whether the quantity specified by the user is valid, essentially if there is enough stock"""

        for InventoryItem in self.OrderCreation.Inventory:
            if InventoryItem.ItemID == self.ItemID:

                """Checks if reducing the stock by amount specified will cause stock to become a negative integer"""
                if (InventoryItem.Stock - self.Quantity >= 0) and (self.Quantity > 0):

                    """Reduces the stock of the inventory item but does not save, in case order isn't finalised"""
                    InventoryItem.Stock -= self.Quantity
                    return True
                else:
                    message.showerror('Error', 'Error whilst adding item, check quantity input', parent=self)
        return False

    def Finished(self, *Event):
        """Called when the FinishedButton is clicked or the return key is pressed to add the item to the order"""
        try:
            self.Quantity = int(self.QuantityEntry.get())
            self.ItemID = self.InventorySelection.GetSelectedItem()[0]

            """Checks whether there is enough stock to meet required quantity"""
            if self.ValidField():
                """Creates a new OrdersItem object and appends it to the master class Orders array"""
                self.OrderCreation.Order.append(
                    OrdersItem(self.OrderCreation.Order.OrderID, self.ItemID, self.Quantity))

                """Reloads the Order tree in the main interface by calling a master class function"""
                self.OrderCreation.LoadOrderTree(self.OrderCreation.Order)

                """Destroys the InventorySelection and QuantitySelection GUI instances now the item has been added"""
                self.InventorySelection.destroy()
                self.destroy()
        except ValueError as E:
            message.showerror('Error', 'Error whilst adding item: ' + str(E), parent=self)


class CustomerSelection(Toplevel):
    """Creates an instance of the CustomerSelection interface as subclass of TopLevel with OrderCreation as root"""

    def __init__(self, *args, **kwargs):
        """Parameters are passed onto the Tkinter parent Frame class"""
        super().__init__(**kwargs)

        """Setting the master class as the argument passed when the class was called, will be OrderCreation"""
        self.OrderCreation = args[0]

        """Sets the window title of the new TopLevel instance"""
        self.title('Customer Selection')

        """Calls class defined functions to load database, set up interface and load customers tree"""
        self.LoadDatabase()
        self.LoadInterface()
        self.LoadCustomers()

    def LoadDatabase(self):
        """Called to create connection to Database type specified in the configuration file and reads data"""

        self.Customers = []

        """Creates Customer object for each row found in Database and places object in new Customers array"""
        Records = database.Connect('Customers').Read()
        for Record in Records:
            self.Customers.append(Customer(Record[0], Record[1], Record[2], Record[3], Record[4]))

    def LoadInterface(self):
        """Creates and packs the CustomerFrame widget onto the root interface using the pack geometry manager"""
        self.CustomerFrame = LabelFrame(self, text='Customers')
        self.CustomerFrame.pack(fill=BOTH, expand=TRUE, side=RIGHT)

        """Creates and packs the CustomerActions widget onto the CustomerFrame frame using the pack geometry manager"""
        self.CustomerActions = Frame(self.CustomerFrame)
        self.CustomerActions.pack(fill=BOTH, expand=TRUE, anchor=W, padx=5, pady=5)

        """Creates and packs a new Button onto the CustomerActions frame and assigns a command"""
        self.NewButton = Button(self.CustomerActions, text='New', command=lambda: NewCustomer(self, self.OrderCreation))
        self.NewButton.grid(row=0, column=0)

        """Creates and packs Treeview widget onto the CustomerFrame frame, binds functions and hides headings"""
        self.CustomerTree = Treeview(self.CustomerFrame, height=20)
        self.CustomerTree.pack(side=LEFT, expand=TRUE, fill=BOTH)
        self.CustomerTree.bind('<<TreeviewSelect>>', self.Finished)
        self.CustomerTree['show'] = 'headings'

        """Creates Scrollbar widget and packs it beside Treeview on the CustomerFrame and assigns scroll command"""
        self.CustomerTreeScrollbar = Scrollbar(self.CustomerFrame, command=self.CustomerTree.yview)
        self.CustomerTreeScrollbar.pack(side=RIGHT, fill=Y)
        self.CustomerTree.config(yscrollcommand=self.CustomerTreeScrollbar.set)

        """Specifies the Attributes and Headers for each Treeview column/row"""
        self.CustomerAttributes = ('id', 'firstname', 'surname', 'contact', 'address')
        self.CustomerHeaders = ('ID', 'Firstname', 'Surname', 'Contact', 'Address')
        self.CustomerTree['columns'] = self.CustomerAttributes

        """Creates each column in Treeview for each item in Headers array, specifying title, anchor and length"""
        for Header in self.CustomerHeaders:
            self.CustomerTree.heading(self.CustomerAttributes[self.CustomerHeaders.index(Header)], text=Header,
                                      anchor=W)
            self.CustomerTree.column(self.CustomerAttributes[self.CustomerHeaders.index(Header)], width=140,
                                     minwidth=140)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadCustomers(self):
        """Called to load the Treeview widget with the data in list specified in the parameter"""

        """Inserts a new item with values specified using record attributes"""
        for Record in self.Customers:
            self.CustomerTree.insert('', END, text=self.Customers.index(Record), values=(Record.GetAttributes()))

    def GetSelectedCustomer(self):
        """Returns the values for the customer is currently selected in the Treeview"""

        for Selection in self.CustomerTree.selection():
            Selected = self.CustomerTree.item(Selection)
            return Selected['values']

    def Finished(self, Event):
        """Called when the Treeview item is selected using the <<TreeviewSelect>> binding, assigns customer to order"""

        """Sets the the master class Order object's CustomerID as the customer ID in the select tree item"""
        self.OrderCreation.Order.CustomerID = self.GetSelectedCustomer()[0]

        """Changes the view of the select customer button now a customer has been selected"""
        self.OrderCreation.CustomerButton['state'] = DISABLED
        self.OrderCreation.CustomerButton['text'] = 'Selected'

        """Destroys the GUI instance now a customer object has been assigned to the order"""
        self.destroy()


class NewCustomer(Toplevel):
    """Creates an instance of the NewCustomer interface as a subclass of TopLevel with Inventory as root"""

    def __init__(self, *args, **kwargs):
        """Parameters are passed onto the Tkinter parent Frame class"""
        super().__init__(**kwargs)

        """Setting the master class as the argument passed when the class was called, will be CustomerSelection"""
        self.CustomerSelection = args[0]

        """Setting the master class of the master class which will be OrderCreation"""
        self.OrderCreation = args[1]

        """Sets the window title of the new TopLevel instance"""
        self.title('New customer')

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

        """As the ID entry should be unique, it is auto-generated based on existing customer data"""
        self.IDEntry.insert(0, self.GenerateID())

        """Sets entry in first index to disabled state after it's loaded so it cannot be edited by the user"""
        self.IDEntry.configure(state=DISABLED)

        """Binds the return key to call the Finished function"""
        self.bind('<Return>', self.Finished)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def GenerateID(self):
        """Returns the unique ID the new customer be stored as, checks through existing customer data"""

        """Definite iteration through Customers array checking if generated ID already exists"""
        GeneratedID = 1
        for Customer in self.CustomerSelection.Customers:

            """If generated ID does not exist for this customer, it is available so return the generated number"""
            if int(Customer.CustomerID) is not GeneratedID:
                return GeneratedID

            """Else add one to generated ID and reiterate"""
            GeneratedID += 1

        """Final number should be available as it will be the final generated ID plus one"""
        return GeneratedID

    def ValidFields(self):
        """Checks whether the fields specified by the user are valid and Customer objects can be made"""

        try:
            Customer(int(self.Input[0]), self.Input[1], self.Input[2], self.Input[3], self.Input[4])
            return True
        except ValueError as E:
            message.showerror('Error', 'Check fields for error: ' + str(E), parent=self)
            return False

    def Finished(self):
        """Called when the FinishedButton is clicked or the return key is pressed to assign new customer"""

        """Gathers all entry values and appends it to new Input array"""
        self.Entries = [self.IDEntry, self.FirstnameEntry, self.SurnameEntry, self.ContactEntry, self.AddressEntry]
        self.Input = []
        for Entry in self.Entries:
            self.Input.append(Entry.get())

        """Calls function to see if all values are valid before continuing"""
        if self.ValidFields():
            """Inserts newly created Customer into the database using user inputs"""
            database.Connect('Customers').Insert(
                Customer(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4]))

            """Sets the the OrderCreation class Order object's CustomerID as the customer ID in the select tree item"""
            self.OrderCreation.Order.CustomerID = self.Input[0]

            """Changes the view of the select customer button now a customer has been selected"""
            self.OrderCreation.CustomerButton['state'] = DISABLED
            self.OrderCreation.CustomerButton['text'] = 'Selected'

            """Destroys the CustomerSelection and NewCustomer GUI instances now the item has been added"""
            self.CustomerSelection.destroy()
            self.destroy()
