import csv
import os
from tkinter import *
from tkinter import filedialog as dialog
from tkinter import messagebox as message
from tkinter.ttk import *

from src import database
from src.utils import *


class Item:
    """Creates an object to be stored in the Inventory array"""

    def __init__(self, ItemID, Brand, Type, Name, Price, Stock):
        """Parameters stored as attributes for each Inventory item"""

        self.ItemID = int(ItemID)
        self.Brand = str(Brand)
        self.Type = str(Type)
        self.Name = str(Name)
        self.Price = float(Price)
        self.Stock = int(Stock)

    def GetAttributes(self):
        """Returns the the attributes of the Item object as a list"""

        return int(self.ItemID), self.Brand, self.Type, self.Name, float('{0:.2f}'.format(self.Price)), int(self.Stock)

    def GetID(self):
        return int(self.ItemID)


class InventoryManager(Toplevel):
    """Creates an instance of the InventoryManager interface as a subclass of the Tkinter Toplevel widget"""

    def __init__(self, *args, **kwargs):
        """Initialises the different features for the application"""

        """Setting the master class as the argument passed when the class was called, will be Main Menu root instance"""
        self.master = args[0]

        """Parameters are passed onto the Tkinter parent Toplevel class"""
        super().__init__(**kwargs)

        """Sets application title"""
        self.title('Inventory Management')

        """Calls class defined functions to connect to database, set up interface and inventory items"""
        self.LoadDatabase()
        self.LoadInterface()
        self.LoadInventory(self.Inventory)

        """Starts the main loop for the application"""
        self.mainloop()

    def LoadDatabase(self):
        """Called to create connection to Database type specified in the configuration file and reads data"""

        self.Inventory = []

        """Creates Item object for each row found in Database and places object in new Inventory array"""
        Records = database.Connect('Inventory').Read()
        for Record in Records:
            NewItem = Item(Record[0], Record[1], Record[2], Record[3], Record[4], Record[5])
            self.Inventory.append(NewItem)

    def LoadInterface(self):
        """Called to set up the core interface widgets for the application"""

        """Creates and packs the Frame widget onto the root interface using the pack geometry manager"""
        self.TopFrame = Frame(self)
        self.TopFrame.pack(fill=BOTH)

        """Creates and packs the Frame widgets onto the TopFrame frame using the pack geometry manager"""
        self.LeftLabelWidgets = Frame(self.TopFrame)
        self.LeftLabelWidgets.pack(side=LEFT)
        self.LeftEntryWidgets = Frame(self.TopFrame)
        self.LeftEntryWidgets.pack(side=LEFT)
        self.RightLabelWidgets = Frame(self.TopFrame)
        self.RightLabelWidgets.pack(side=LEFT)
        self.RightEntryWidgets = Frame(self.TopFrame)
        self.RightEntryWidgets.pack(side=LEFT)

        """Creates and packs the LabelFrame widgets onto the TopFrame frame using the pack geometry manager"""
        self.ButtonWidgets = LabelFrame(self.TopFrame, text='Actions')
        self.ButtonWidgets.pack(side=RIGHT)
        self.SearchWidgets = LabelFrame(self.TopFrame, text='Search:')
        self.SearchWidgets.pack(side=TOP, pady=35)

        """Creates and packs the Label widgets onto the LeftLabelWidgets frame using the pack geometry manager"""
        self.IDLabel = Label(self.LeftLabelWidgets, text='ID:')
        self.IDLabel.pack(anchor=W, padx=6, pady=6)
        self.BrandLabel = Label(self.LeftLabelWidgets, text='Brand:')
        self.BrandLabel.pack(anchor=W, padx=6, pady=6)
        self.TypeLabel = Label(self.LeftLabelWidgets, text='Type:')
        self.TypeLabel.pack(anchor=W, padx=6, pady=6)
        self.NameLabel = Label(self.LeftLabelWidgets, text='Name:')
        self.NameLabel.pack(anchor=W, padx=6, pady=6)

        """Creates and packs the Label widgets onto the RightLabelWidgets frame using the pack geometry manager"""
        self.PriceLabel = Label(self.RightLabelWidgets, text='Price:')
        self.PriceLabel.pack(anchor=W, padx=6, pady=6)
        self.StockLabel = Label(self.RightLabelWidgets, text='Stock:')
        self.StockLabel.pack(anchor=W, padx=6, pady=6)

        """Creates and packs extra Label widget used for perfect GUI placement"""
        self.Placeholder = Label(self.RightLabelWidgets)
        self.Placeholder.pack(anchor=W, padx=6, pady=6)

        """Creates and packs the Entry widgets onto the LeftEntryWidgets frame using the pack geometry manager"""
        self.IDEntry = Entry(self.LeftEntryWidgets, width=15)
        self.IDEntry.pack(anchor=W, padx=5, pady=5)
        self.BrandEntry = Entry(self.LeftEntryWidgets, width=15)
        self.BrandEntry.pack(anchor=W, padx=5, pady=5)
        self.TypeEntry = Entry(self.LeftEntryWidgets, width=15)
        self.TypeEntry.pack(anchor=W, padx=5, pady=5)
        self.NameEntry = Entry(self.LeftEntryWidgets, width=15)
        self.NameEntry.pack(anchor=W, padx=5, pady=5)

        """Creates and packs the Entry widgets onto the RightEntryWidgets frame using the pack geometry manager"""
        self.PriceEntry = Entry(self.RightEntryWidgets, width=15)
        self.PriceEntry.pack(anchor=W, padx=5, pady=5)
        self.StockEntry = Entry(self.RightEntryWidgets, width=15)
        self.StockEntry.pack(anchor=W, padx=5, pady=5)

        """Creates and packs a Button onto the same frame using the pack geometry manager"""
        self.SaveButton = Button(self.RightEntryWidgets, text='Save', command=self.SaveItemAttributes)
        self.SaveButton.pack(anchor=CENTER, padx=3, pady=3)

        """Specifies the different search options available and creates a variable for the users selection"""
        self.SearchOptions = ('ID', 'Brand', 'Type', 'Name', 'Price', 'Stock')
        self.SearchVariable = StringVar()
        self.SearchVariable.set(self.SearchOptions[3])

        """Creates an OptionMenu widget and packs it onto the SearchWidgets frame using the pack geometry manager"""
        self.SearchOptionsMenu = OptionMenu(self.SearchWidgets, self.SearchVariable, '', *self.SearchOptions)
        self.SearchOptionsMenu.config(width='15')
        self.SearchOptionsMenu.pack()

        """Creates an Entry widget, packs it onto the SearchWidgets frame, then binds a keyboard action to a function"""
        self.SearchEntry = Entry(self.SearchWidgets)
        self.SearchEntry.pack(anchor=CENTER)
        self.SearchEntry.bind('<KeyRelease>', self.Search)

        """Creates and packs the Button widgets onto the ButtonWidgets frame then assigns specific function commands"""
        self.AddButton = Button(self.ButtonWidgets, text='New', command=lambda: NewItem(self))
        self.AddButton.pack(anchor=CENTER, padx=1, pady=1)
        self.DeleteButton = Button(self.ButtonWidgets, text='Remove', command=self.DeleteItem)
        self.DeleteButton.pack(anchor=CENTER, padx=1, pady=1)
        self.RefreshButton = Button(self.ButtonWidgets, text='Refresh', command=self.RefreshItems)
        self.RefreshButton.pack(anchor=CENTER, padx=1, pady=1)
        self.ImportButton = Button(self.ButtonWidgets, text='Import', command=self.ImportItems)
        self.ImportButton.pack(anchor=CENTER, padx=1, pady=1)
        self.ExportButton = Button(self.ButtonWidgets, text='Export', command=self.ExportItems)
        self.ExportButton.pack(anchor=CENTER, padx=1, pady=1)

        """Creates and packs the Frame widget onto the root interface using the pack geometry manager, below TopFrame"""
        self.BottomFrame = LabelFrame(self, text='Inventory')
        self.BottomFrame.pack(fill=BOTH, expand=TRUE)

        """Creates and packs Treeview widget onto the BottomFrame frame, binds functions and hides headings"""
        self.InventoryTreeview = Treeview(self.BottomFrame, height=19)
        self.InventoryTreeview.pack(side=LEFT, expand=TRUE, fill=BOTH)
        self.InventoryTreeview.bind('<<TreeviewSelect>>', self.LoadItemAttributes)
        self.InventoryTreeview.bind('<Button-1>', self.ClickTree)
        self.InventoryTreeview['show'] = 'headings'

        """Creates Scrollbar widget and packs it beside Treeview on the BottomFrame and assigns scroll command"""
        self.InventoryTreeviewScrollbar = Scrollbar(self.BottomFrame, command=self.InventoryTreeview.yview)
        self.InventoryTreeviewScrollbar.pack(side=RIGHT, fill=Y)
        self.InventoryTreeview.config(yscrollcommand=self.InventoryTreeviewScrollbar.set)

        """Specifies the Attributes and Headers for each Treeview column/row"""
        self.Attributes = ('id', 'brand', 'type', 'name', 'price', 'stock')
        self.Headers = ('ID', 'Brand', 'Type', 'Name', 'Price', 'Stock')
        self.InventoryTreeview['columns'] = self.Attributes

        """Creates each column in Treeview for each item in Headers array, specifying title, anchor and length"""
        for Header in self.Headers:
            self.InventoryTreeview.heading(self.Attributes[self.Headers.index(Header)], text=Header, anchor=W)
            self.InventoryTreeview.column(self.Attributes[self.Headers.index(Header)], width=135, minwidth=135)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def LoadInventory(self, Data):
        """Called to load the Treeview widget with the data in list specified in the parameter"""

        """Calls function to remote all of the items already existing in the Treeview widget"""
        self.ResetInventory()

        """Inserts a new item at index i with values specified as long as there is an item in the Data parameter"""
        if Data:
            i = 0
            for Record in Data:
                self.InventoryTreeview.insert('', END, text=i, values=(Record.GetAttributes()))
                i += 1

            """Sets the current selected item as the first value which will also trigger the TreeviewSelect function"""
            self.InventoryTreeview.selection_set(self.InventoryTreeview.get_children()[0])

    def SaveInventory(self, Data):
        """Called to save the data stored in the class defined Data list in the database"""

        database.Connect('Inventory').Save(Data)

    def ResetInventory(self):
        """Called to remove all the items already stored inside the Treeview widget"""

        self.InventoryTreeviewChildren = self.InventoryTreeview.get_children()
        for Child in self.InventoryTreeviewChildren:
            self.InventoryTreeview.delete(Child)

    def ClickTree(self, Event):
        """Called to change the Treeview to a different sort type, activated by clicking header using Event parameter"""

        """Function is called for every click on Treeview so checks whether click region is header"""
        self.ClickedRegion = self.InventoryTreeview.identify('region', Event.x, Event.y)
        if self.ClickedRegion == 'heading':
            """Calls function to load the inventory with a sorted list"""
            self.LoadInventory(SortTree(Event, self.InventoryTreeview, self.Inventory))

    def GetSelectedItem(self):
        """Returns the values for the item dictionary which is currently selected in the Treeview"""

        self.Selected = self.InventoryTreeview.selection()
        for Item in self.Selected:
            self.SelectedIndex = self.InventoryTreeview.item(Item)
            self.SelectedRecord = self.SelectedIndex['values']
        return self.SelectedRecord

    def LoadItemAttributes(self, Event):
        """Called when an item is clicked in the Treeview to update all Entries in above frame"""

        """Enables ID entry so it can be loaded with data"""
        self.IDEntry.configure(state=ACTIVE)

        """Creates a new list and places all the entries previously specified for easy iteration"""
        self.Entries = [self.IDEntry, self.BrandEntry, self.TypeEntry, self.NameEntry, self.PriceEntry, self.StockEntry]

        """Definite iteration through Entries list to reset contents and add the values of selected item"""
        for Entry in self.Entries:
            Entry.delete(0, END)
            Entry.insert(END, self.GetSelectedItem()[self.Entries.index(Entry)])

        """Sets entry in first index to disabled state after it's loaded so it cannot be edited by the user"""
        self.Entries[0].configure(state=DISABLED)

    def SaveItemAttributes(self):
        """Called when the Save button is pressed, used to save the values specified in the Entries"""

        """Places all values stored in all Entry widgets into new Input array"""
        self.Input = []
        for Entry in self.Entries:
            self.Input.append(Entry.get())

        """If edit entries are valid, continue on to edit the item"""
        if self.ValidFields():

            """Creates a new object based off items stored in the Input array"""
            self.NewItem = Item(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4],
                                self.Input[5])

            """Gets the ID attribute of the selected Treeview item"""
            self.SelectedID = self.GetSelectedItem()[0]

            """Changes the Item identified by the ID attribute to the new NewItem object"""
            for DataItem in self.Inventory:
                if DataItem.GetAttributes()[0] == self.SelectedID:
                    self.Inventory[self.Inventory.index(DataItem)] = self.NewItem

            """Edits the same item which is stored in the Treeview to the same values"""
            for Entry in self.Entries:
                self.InventoryTreeview.set(self.Selected[0], column=self.Entries.index(Entry), value=Entry.get())

            """Calls the class defined method to save inventory Data now that an item has been edited"""
            self.SaveInventory(self.Inventory)

    def ValidFields(self):
        """Returns whether it is possible to create valid item to store in inventory"""

        """Attempts to create Item object using provided input, returns true if possible or error if not"""
        try:
            Item(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4], self.Input[5])
            return True
        except ValueError as E:
            message.showerror('Error', 'Check fields for error: ' + str(E), parent=self)
            return False

    def Search(self, Event):
        """Called when the SearchEntry is edited using the <KeyRelease> binding"""

        """Gets the user input of the SearchEntry widget and the SearchVariable (OptionsMenu choice)"""
        self.Query = self.SearchEntry.get()
        self.Attribute = self.SearchVariable.get()

        """Creates a new array to store the results of the search attempt"""
        self.Results = []

        """Definite iteration checking each item in the Data array with input specified in the Entry and OptionsMenu"""
        for DataItem in self.Inventory:
            if str(self.Query).lower() in \
                    str(DataItem.GetAttributes()[(self.SearchOptions.index(self.Attribute))]).lower():
                """Append the Item object to the results array if the condition is met"""
                self.Results.append(DataItem)

        """Calls the function to load the Treeview widget with the Results list"""
        self.LoadInventory(self.Results)

        """As long as there is at least one result, set the first option in the Treeview widget"""
        if self.Results:
            self.InventoryTreeview.selection_set(self.InventoryTreeview.get_children()[0])

    def DeleteItem(self):
        """Called when the Remove button is pressed, used to remove the selected item from the inventory"""

        """Gets the values of the selected Treeview item"""
        self.SelectedRecord = self.GetSelectedItem()

        """Prompts the user for removal confirmation and will continue if the user selects YES"""
        Confirm = message.askquestion('Remove', 'Remove item from inventory?', icon='warning', parent=self)
        if Confirm == message.YES:

            """Definite iteration through inventory Data looking for selected item"""
            for DataItem in self.Inventory:
                if int(DataItem.ItemID) == int(self.SelectedRecord[0]):
                    """Removes item from Data list as well as Treeview when match is found"""
                    self.Inventory.remove(DataItem)
                    self.InventoryTreeview.delete(self.Selected[0])

            """Calls the class defined method to save inventory Data now that an item has been removed"""
            self.SaveInventory(self.Inventory)

            """As long as there is at least one result, set the first option in the Treeview widget"""
            if self.Inventory:
                self.InventoryTreeview.selection_set(self.InventoryTreeview.get_children()[0])

    def RefreshItems(self):
        """Called when the Refresh button is pressed, used to save and refresh the inventory"""

        self.SaveInventory(self.Inventory)
        self.LoadInventory(self.Inventory)

    def ImportItems(self, *Event):
        """Called when the Import button is pressed, allows user to import a .csv file as the inventory list"""

        """Will attempt to read selected import file, returns error if not possible"""
        try:

            """User to prompted for csv file to import"""
            File = dialog.askopenfile(mode='r+', title='Import file', parent=self, defaultextension='.csv',
                                      filetypes=[('CSV file', '.csv'), ('Text file', '.txt')])

            """Creates instance to read specified csv file"""
            Reader = csv.reader(File)

            """Creates new array to store records found in csv file"""
            ImportedItems = []

            """Iteration through csv file which creates an Item object for each record then appends it to new array"""
            for Record in Reader:
                if Record:
                    try:
                        ImportItem = Item(int(Record[0]), str(Record[1]), str(Record[2]), str(Record[3]),
                                          float(Record[4]), int(Record[5]))
                        ImportedItems.append(ImportItem)
                    except ValueError as E:
                        message.showerror('Error', 'Error whilst importing: ' + str(E), parent=self)
                        return

            """User is prompted to confirm whether they wish to replace existing inventory"""
            Confirm = message.askquestion('Confirm', 'Old list will be wiped and replaced with new list, are you sure?',
                                          icon='warning', parent=self)

            """If user selects YES, existing inventory will be replaced and message will be displayed"""
            if Confirm == message.YES:
                self.Inventory = ImportedItems
                message.showinfo('Import', 'Successfully imported ' + File.name, parent=self)
        except (ValueError, TypeError, FileNotFoundError) as E:
            message.showerror('Error', 'Error whilst importing: ' + str(E), parent=self)
        finally:

            """Will finally call RefreshItems function which saves and loads the inventory list"""
            self.RefreshItems()

    def ExportItems(self):
        """Called when the Export button is pressed, allows user to export the inventory to .csv file"""

        """Will attempt to write data to exported file, returns error if not possible"""
        try:

            """User to prompted for destination and file name to save the exported file"""
            File = dialog.asksaveasfile(parent=self, mode='w', defaultextension='.csv',
                                        initialfile='inventory.csv', title='Export file')

            """Creates instance to write csv file at specified location"""
            Writer = csv.writer(File)

            """Writes the attributes of each Item in the inventory to the csv file specified if Data exists"""
            if self.Inventory:
                for DataItem in self.Inventory:
                    Writer.writerow(DataItem.GetAttributes())

            """Close the file instance created previously"""
            File.close()

            """User is prompted whether they wish to open the created file and will do so if user selects YES"""
            Confirm = message.askquestion('Open file', 'Open ' + File.name + ' in notepad?', parent=self)
            if Confirm == message.YES:
                os.system('notepad.exe ' + File.name)
        except TypeError as E:
            message.showerror('Error', 'Error whilst exporting: ' + str(E), parent=self)


class NewItem(Toplevel):
    """Creates an instance of the New interface as a subclass of the Tkinter TopLevel widget with Inventory as root"""

    def __init__(self, *args, **kwargs):
        """Parameters are passed onto the Tkinter parent Frame class"""
        super().__init__(**kwargs)

        """Setting the master class as the argument passed when the class was called, will be Inventory"""
        self.master = args[0]

        """Sets the window title of the new TopLevel instance"""
        self.title('New item')

        """Calls class defined functions to set up interface"""
        self.LoadInterface()

    def LoadInterface(self):
        """Creates and packs the MainFrame widget onto the root interface using the pack geometry manager"""

        self.MainFrame = Frame(self)
        self.MainFrame.pack()

        """Creates and packs the Label widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDLabel = Label(self.MainFrame, text='ID:')
        self.IDLabel.grid(row=0, column=0, sticky=W, padx=10)
        self.BrandLabel = Label(self.MainFrame, text='Brand:')
        self.BrandLabel.grid(row=1, column=0, sticky=W, padx=10)
        self.TypeLabel = Label(self.MainFrame, text='Type:')
        self.TypeLabel.grid(row=2, column=0, sticky=W, padx=10)
        self.NameLabel = Label(self.MainFrame, text='Name:')
        self.NameLabel.grid(row=3, column=0, sticky=W, padx=10)
        self.PriceLabel = Label(self.MainFrame, text='Price:')
        self.PriceLabel.grid(row=4, column=0, sticky=W, padx=10)
        self.StockLabel = Label(self.MainFrame, text='Stock:')
        self.StockLabel.grid(row=5, column=0, sticky=W, padx=10)

        """Creates and packs the Entry widgets onto the MainFrame frame using the grid geometry manager"""
        self.IDEntry = Entry(self.MainFrame, width=25)
        self.IDEntry.grid(row=0, column=1, padx=10, pady=5)
        self.BrandEntry = Entry(self.MainFrame, width=25)
        self.BrandEntry.grid(row=1, column=1, padx=10, pady=5)
        self.TypeEntry = Entry(self.MainFrame, width=25)
        self.TypeEntry.grid(row=2, column=1, padx=10, pady=5)
        self.NameEntry = Entry(self.MainFrame, width=25)
        self.NameEntry.grid(row=3, column=1, padx=10, pady=5)
        self.PriceEntry = Entry(self.MainFrame, width=25)
        self.PriceEntry.grid(row=4, column=1, padx=10, pady=5)
        self.StockEntry = Entry(self.MainFrame, width=25)
        self.StockEntry.grid(row=5, column=1, padx=10, pady=5)

        """Creates a new button and packs it onto the MainFrame frame using the grid geometry manager """
        self.FinishedButton = Button(self.MainFrame, text='Finished', command=self.Finished)
        self.FinishedButton.grid(row=6, columnspan=2, pady=5)

        """As the ID entry should be unique, it is auto-generated based on the items existing in the Data"""
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
        for DataItem in self.master.Inventory:

            """If generated ID does not exist for this item, it is available so return the generated number"""
            if int(DataItem.ItemID) is not int(GeneratedID):
                return GeneratedID

            """Else add one to generated ID and reiterate"""
            GeneratedID += 1

        """Final number should be available as it will be the final generated ID plus one"""
        return GeneratedID

    def ValidFields(self):
        """Returns whether it is possible to create valid item to store in inventory"""

        """Attempts to create Item object using provided input, returns true if possible or error if not"""
        try:
            Item(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4], self.Input[5])
            return True
        except ValueError as E:
            message.showerror('Error', 'Check fields for error: ' + str(E), parent=self)
            return False

    def Finished(self):
        """Called when the user presses the Finished button, used to save the new item"""

        """Creates a new list and places all the entries previously specified for easy usage"""
        self.Entries = [self.IDEntry, self.BrandEntry, self.TypeEntry, self.NameEntry, self.PriceEntry, self.StockEntry]

        """Creates a new list and appends all the values from all Entry widgets stored in the Entries list"""
        self.Input = []
        for Entry in self.Entries:
            self.Input.append(Entry.get())

        """If input entries are valid, continue on to add the item"""
        if self.ValidFields():
            """Creates a new Item object using the all indexes specified in the Inputs list"""
            self.NewItem = Item(self.Input[0], self.Input[1], self.Input[2], self.Input[3], self.Input[4],
                                self.Input[5])

            """Adds item into data list using built in insert function, inserts at the first location relevant to ID"""
            self.master.Inventory.insert(int(self.Input[0]) - 1, self.NewItem)

            """Calls the class defined method in Inventory to save inventory Data now that an item has been added"""
            self.master.SaveInventory(self.master.Inventory)

            """Calls the class defined method in Inventory to update the Treeview with the inventory data"""
            self.master.LoadInventory(self.master.Inventory)

            """Built-in defined method used to destroy the New interface"""
            self.destroy()
