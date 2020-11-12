import tkinter as tk
from tkinter import *
from tkinter import messagebox as message
from tkinter.ttk import *

from src import database
from src.utils import *


class Order(list):
    """Creates an object to be stored as each order, acts as a list with main attributes in parameters"""

    def __init__(self, OrderID, Date, CustomerID, OrdersItems):
        """Parameters are passed onto the List class"""
        super().__init__(OrdersItems)

        """Parameters stored as attributes for each Order item"""
        self.OrderID = OrderID
        self.Date = Date
        self.CustomerID = CustomerID

    def GetCustomerAttributes(self):
        """Returns the relevant customer information a list"""

        Records = database.Connect('Customers').Read()
        for Record in Records:
            if int(Record[0]) == int(self.CustomerID):
                return Record

    def GetAttributes(self):
        """Returns the attributes of the Order object as a list"""

        return int(self.OrderID), self.Date

    def GetID(self):
        """Returns the unique ID of the object"""

        return int(self.OrderID)


class OrderItem:
    """Creates an object item to be stored in order objects"""

    def __init__(self, OrderID, ItemID, Quantity):
        """Parameters stored as attributes for each OrderItem item"""

        self.OrderID = OrderID
        self.ItemID = ItemID
        self.Quantity = Quantity

    def GetAttributes(self):
        """Returns the attributes of the OrderItem object as a list"""

        return int(self.OrderID), int(self.ItemID), int(self.Quantity)

    def GetID(self):
        """Returns the unique ID of the object"""

        return int(self.ItemID)


class OrderManager(Toplevel):
    """Creates an instance of the OrderManager interface as a subclass of the Tkinter Toplevel widget"""

    def __init__(self, *args, **kwargs):
        """Initialises the different features for the application"""

        """Setting the master class as the argument passed when the class was called, will be Main Menu root instance"""
        self.master = args[0]

        """Parameters are passed onto the Tkinter parent Toplevel class"""
        super().__init__(**kwargs)

        """Sets application title"""
        self.title('Order Management')

        """Calls class defined functions to connect to database, set up interface and inventory items"""
        self.LoadDatabase()
        self.LoadInterface()
        self.LoadOrdersList(self.Orders)

        """Starts the main loop for the application"""
        self.mainloop()

    def LoadDatabase(self):
        """Called to create connection to Database type specified in the configuration file, read and store data"""

        self.Orders = []

        """Creates Order object for each row found in Database"""
        Records = database.Connect('Orders').Read()
        for Record in Records:
            """Creates a new Order object with the attributes found in database, also creates new array of OrdersItem"""
            NewOrder = Order(Record[0], Record[1], Record[2], Record[3], self.LoadOrdersItems(Record[0]))

            """Places new Order object into the new Orders array, each Order has the main attributes and OrdersItem"""
            self.Orders.append(NewOrder)

    def LoadOrdersItems(self, OrderID):
        """Returns an array of relevant OrdersItem for the Order ID specified in the parameters"""

        """Creates new array to store new OrdersItem for specified Order"""
        self.OrdersItems = []

        """Similar connection is made to a second database"""
        Records = database.Connect('OrdersItem').Read()
        for Record in Records:
            if Record[0] == OrderID:
                """Appends a new OrderItem object into OrdersItem array using data found in database"""
                self.OrdersItems.append(OrderItem(Record[0], Record[1], Record[2]))
        return self.OrdersItems

    def LoadInterface(self):
        """Called to set up the core interface widgets for the application"""

        """Creates and packs the LabelFrame widgets onto the root interface using the pack geometry manager"""
        self.OrdersFrame = LabelFrame(self, text='Order')
        self.OrdersFrame.pack(side=LEFT, fill=BOTH)
        self.OrderDetailFrame = LabelFrame(self, text='Information')
        self.OrderDetailFrame.pack(side=BOTTOM, expand=TRUE, fill=BOTH)

        """Creates and packs the Frame widgets onto the OrdersFrame frame using the pack geometry manager"""
        self.OrdersSearchFrame = Frame(self.OrdersFrame)
        self.OrdersSearchFrame.pack()
        self.OrdersListFrame = Frame(self.OrdersFrame)
        self.OrdersListFrame.pack(expand=TRUE, fill=BOTH)

        """Creates and packs the Entry widget onto the OrdersSearchFrame, binds a key and focuses input on the entry"""
        self.SearchEntry = Entry(self.OrdersSearchFrame)
        self.SearchEntry.grid(row=0, column=0)
        self.SearchEntry.bind('<KeyRelease>', self.Search)
        self.SearchEntry.focus_force()

        """Creates a Button and PhotoImage widget, changes the appearance of the Button to the image, assigns command"""
        self.DeleteButton = tk.Button(self.OrdersSearchFrame, command=self.DeleteOrder, width=11, height=13,
                                      state="disabled")
        self.DeleteImageResource = PhotoImage(master=self, file='../Data/Resources/Orders/Delete.png')
        self.DeleteButton['image'] = self.DeleteImageResource
        self.DeleteButton.grid(row=0, column=1, sticky=N + E + S + W)

        """Creates ListBox widget and packs it using pack geometry manager, then binds command when item is selected"""
        self.OrderListbox = Listbox(self.OrdersListFrame, highlightthickness=0, activestyle=DOTBOX,
                                    exportselection=FALSE)
        self.OrderListbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.OrderListbox.bind('<<ListboxSelect>>', self.LoadOrderInformation)

        """Creates Scrollbar widget and packs it beside ListBox on the OrdersListFrame and assigns scroll command"""
        self.OrderListboxScrollbar = Scrollbar(self.OrdersListFrame, command=self.OrderListbox.yview)
        self.OrderListboxScrollbar.pack(side=RIGHT, fill=BOTH, expand=FALSE)
        self.OrderListbox.config(yscrollcommand=self.OrderListboxScrollbar.set)

        """Creates and packs Frame widgets onto the OrderDetailFrame using pack geometry manager"""
        self.OrderAttributes = Frame(self.OrderDetailFrame)
        self.OrderAttributes.pack(side=TOP, fill=BOTH, pady=5)
        self.OrderItemDetails = LabelFrame(self.OrderDetailFrame, text='Items')
        self.OrderItemDetails.pack(side=BOTTOM, expand=TRUE, fill=BOTH)

        """Creates and packs Frame and LabelFrame widgets on OrderAttributes Frame using the grid geometry manager"""
        self.OrderDetailFrame = Frame(self.OrderAttributes)
        self.OrderDetailFrame.grid(row=0, column=0)
        self.CustomerDetails = LabelFrame(self.OrderAttributes, text='Customer Details')
        self.CustomerDetails.grid(row=0, column=1, padx=10)

        """Creates and packs the Label widgets onto the OrderDetailFrame frame using the grid geometry manager"""
        self.IDLabel = Label(self.OrderDetailFrame, text='Order ID:')
        self.IDLabel.grid(row=0, column=0, sticky=W, padx=3)
        self.DateLabel = Label(self.OrderDetailFrame, text='Date:')
        self.DateLabel.grid(row=1, column=0, sticky=W, padx=3)

        """Creates and packs the Entry widgets onto the OrderDetailFrame frame using the grid geometry manager"""
        self.IDEntry = Entry(self.OrderDetailFrame, width=25)
        self.IDEntry.grid(row=0, column=1, padx=10, pady=3)
        self.DateEntry = Entry(self.OrderDetailFrame, width=25)
        self.DateEntry.grid(row=1, column=1, padx=10, pady=3)

        """Creates and packs Treeview widget onto the OrderItemDetails frame, binds functions and hides headings"""
        self.OrdersItemTreeview = Treeview(self.OrderItemDetails, height=19)
        self.OrdersItemTreeview.pack(side=LEFT, expand=TRUE, fill=BOTH)
        self.OrdersItemTreeview.bind('<Button-1>', self.ClickTree)
        self.OrdersItemTreeview['show'] = 'headings'

        """Creates Scrollbar widget and packs it beside Treeview on the OrderItemDetails frame, assigns scroll bar"""
        self.OrdersItemTreeviewScrollbar = Scrollbar(self.OrderItemDetails, command=self.OrdersItemTreeview.yview)
        self.OrdersItemTreeviewScrollbar.pack(side=LEFT, fill=Y)
        self.OrdersItemTreeview.config(yscrollcommand=self.OrdersItemTreeviewScrollbar.set)

        """Specifies the Attributes and Headers for each Treeview column/row then assigns column to Treeview"""
        self.Attributes = ('itemid', 'name', 'price', 'amount', 'net')
        self.Headers = ('Item ID', 'Name', 'Price', 'Amount', 'Net')
        self.OrdersItemTreeview['columns'] = self.Attributes

        """Creates each column in Treeview for each item in Headers array, specifying title, anchor and length"""
        for Header in self.Headers:
            self.OrdersItemTreeview.heading(self.Attributes[self.Headers.index(Header)], text=Header, anchor=W)
            self.OrdersItemTreeview.column(self.Attributes[self.Headers.index(Header)], width=130, minwidth=130)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadOrdersList(self, Data):
        """Used to populate Orders ListBox widget with all Order objects in parameters"""

        """First clears any existing items in ListBox from index '0' to 'END'"""
        self.OrderListbox.delete(0, END)

        """Check to see if Data in parameter exists"""
        if Data:

            """For each Order in Data, insert an item using the OrderID class attribute"""
            for Order in Data:
                self.OrderListbox.insert(END, Order.OrderID)

            """Set the selected item as the first index and load the Order information for the selected item"""
            self.OrderListbox.select_set(0)
            self.LoadOrderInformation()

    def GetSelectedOrderID(self):
        """Returns the name of the selected item in the OrderList, which will be the chosen Order ID"""

        return self.OrderListbox.get(self.OrderListbox.curselection())

    def GetOrder(self, OrderID):
        """Returns the relevant Order stored in the Orders array with the matching ID in the parameter"""

        for Order in self.Orders:
            if Order.OrderID == OrderID:
                return Order

    def LoadOrderInformation(self, *Event):
        """Calls various functions to set up the selected Order information"""

        self.LoadOrderItemTree(self.GetOrder(self.GetSelectedOrderID()))
        self.LoadOrderAttributes(self.GetOrder(self.GetSelectedOrderID()))
        self.LoadCustomerAttributes(self.GetOrder(self.GetSelectedOrderID()))

    def LoadOrderAttributes(self, Order):
        """Called when an Order is selected in the Listbox to update all Entry boxes"""

        """Creates a new list and places all the entries previously specified for easy iteration"""
        self.Entries = [self.IDEntry, self.DateEntry]

        """Definite iteration through Entries list to reset contents and add the attributes of Order in parameters"""
        for Entry in self.Entries:
            Entry.delete(0, END)
            Entry.insert(END, Order.GetAttributes()[self.Entries.index(Entry)])

    def LoadCustomerAttributes(self, Order):
        """Used to populate CustomerDetails frame with relevant customer information"""

        """Destroys existing widgets stored in the CustomerWidgets frame"""
        for Child in self.CustomerDetails.winfo_children():
            Child.destroy()

        """Specifies the different attributes existing for Customers and loads Customer attributes from Order"""
        self.CustomerFields = ['ID', 'Firstname', 'Surname', 'Contact', 'Address']
        self.CustomerAttributes = Order.GetCustomerAttributes()

        """Definite iteration through CustomerFields list"""
        for Field in self.CustomerFields:
            """Create a Label for each field with the Field and the Customer attribute with pack geometry manager"""
            self.Label = Label(self.CustomerDetails,
                               text=Field + ': ' + str(self.CustomerAttributes[self.CustomerFields.index(Field)]))
            self.Label.pack(anchor='w')

    def ResetOrderItemTree(self):
        """Called to remove all the items already stored inside the Treeview widget"""

        self.OrderTreeviewChildren = self.OrdersItemTreeview.get_children()
        for Child in self.OrderTreeviewChildren:
            self.OrdersItemTreeview.delete(Child)

    def LoadOrderItemTree(self, Data):
        """Called to load the Treeview widget with the data in list specified in the parameter"""

        """Calls function to remote all of the items already existing in the Treeview widget"""
        self.ResetOrderItemTree()

        """Check to see if Data exists"""
        if Data:
            i = 0
            for DataItem in Data:
                """Gathers the Item attributes for the OrderItem object such as the Name and Price"""
                Record = self.GetItemDetails(DataItem)

                """Creates new Tuple, calculating the net value of the OrderItem by multiplying quantity and price"""
                Values = (int(Record[0]), str(Record[1]), float(Record[2]), int(DataItem.Quantity),
                          float('{0:.2f}'.format(int(Record[2]) * int(DataItem.Quantity))))

                """Inserts a new item at index i using the Values tuple"""
                self.OrdersItemTreeview.insert('', END, text=i, values=Values)
                i += 1

            """Sets the current selected item as the first value which will also trigger the TreeviewSelect function"""
            self.OrdersItemTreeview.selection_set(self.OrdersItemTreeview.get_children()[0])

    def GetItemDetails(self, OrderItem):
        """Returns the Item ID, Name and Price of the specified OrderItem using the Item ID"""

        """Connection is made to Inventory database to read item data"""
        Records = database.Connect('Inventory').Read()

        """Definite iteration through inventory database"""
        for Record in Records:

            """If Record first index, the ID, matches the parameter Item ID, return attributes of Record"""
            if int(Record[0]) == int(OrderItem.ItemID):
                return int(Record[0]), str(Record[3]), float(Record[4])

    def ClickTree(self, Event):
        """Called to change the Treeview to a different sort type, activated by clicking header using Event parameter"""

        """Function is called for every click on Treeview so checks whether click region is header"""
        self.ClickedRegion = self.OrdersItemTreeview.identify('region', Event.x, Event.y)
        if self.ClickedRegion == 'heading':
            """Calls function to load the order items with a sorted list"""
            self.LoadOrderItemTree(SortTree(Event, self.OrdersItemTreeview, self.GetOrder(self.GetSelectedOrderID())))

    def DeleteOrder(self):
        """Called when the Remove button is pressed, used to remove the selected Order from the data"""

        """Gets the OrderID of the selected ListBox item"""
        self.SelectedRecord = self.GetSelectedOrderID()

        """Prompts the user for removal confirmation and will continue if the user selects YES"""
        Confirm = message.askquestion('Remove', 'Permanently remove order?', icon='warning', parent=self)
        if Confirm == message.YES:

            """Definite iteration through Orders looking for selected Order"""
            for Order in self.Orders:
                if int(Order.OrderID) == int(self.SelectedRecord):
                    """Removes the relevant Order from the Orders array if found"""
                    self.Orders.remove(Order)

            """Connects to database to save inventory Data now that an item has been removed"""
            database.Connect('Orders').Save(self.Orders)

            """Reloads the Orders list with the new Orders list"""
            self.LoadOrdersList(self.Orders)

    def Search(self, Event):
        """Called on <KeyRelease> for the SearchEntry widget, used to update the ListBox with query"""

        """Sets query variable as the input in SearchEntry widget"""
        self.Query = self.SearchEntry.get()

        """Creates a new array to store the results of the search attempt"""
        self.Results = []

        """Definite iteration checking each Order in Orders Data using query to search Order ID"""
        for Order in self.Orders:
            """If Query ID is in selected Order, append Order to results array"""
            if str(self.Query) == str(Order.OrderID):
                self.Results.append(Order)

        """Load orders list with results if any were found, otherwise show all orders"""
        if self.Results:
            self.LoadOrdersList(self.Results)
        else:
            self.LoadOrdersList(self.Orders)
