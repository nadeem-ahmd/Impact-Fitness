from src.customers import *
from src.inventory import *
from src.order_creation import *
from src.orders import *
from src.settings import *


class MainMenu(Tk):
    """Creates an instance of the InventoryManager interface as a subclass of the Tkinter Tk widget"""

    def __init__(self, *args, **kwargs):
        """Initialises the different features for the application"""

        """Parameters are passed onto the Tkinter parent Tk class"""
        super().__init__(**kwargs)

        """Sets application title"""
        self.title('Main Menu')

        """Calls class defined functions to set up the application interface"""
        self.LoadInterface()

        """Disables the ability for window resizing"""
        self.resizable(0, 0)

        """Starts the main loop for the application"""
        self.mainloop()

    def LoadInterface(self):
        """Called to set up the core interface widgets for the application"""

        """Creates and packs a LabelFrame widget onto the root interface using the grid geometry manager"""
        self.Tools = LabelFrame(self, text='Tools')
        self.Tools.grid(row=0, column=0, sticky=N)

        """Creates and packs various Button widgets, loads relevant image file and sets button as loaded image"""
        self.OrderCreation = Button(self.Tools, command=lambda: OrderCreation(self), width=11)
        self.OrderCreation.grid(row=0, column=0)
        self.OrderCreationImage = PhotoImage(master=self, file='../Data/Resources/Main/OrderCreation.png')
        self.OrderCreation['image'] = self.OrderCreationImage

        self.Inventory = Button(self.Tools, command=lambda: InventoryManager(self), width=11)
        self.Inventory.grid(row=1, column=0)
        self.InventoryImage = PhotoImage(master=self, file='../Data/Resources/Main/Inventory.png')
        self.Inventory['image'] = self.InventoryImage

        self.Orders = Button(self.Tools, command=lambda: OrderManager(self), width=11)
        self.Orders.grid(row=2, column=0)
        self.OrderImage = PhotoImage(master=self, file='../Data/Resources/Main/Orders.png')
        self.Orders['image'] = self.OrderImage

        self.Customers = Button(self.Tools, width=11, command=lambda: CustomerManager(self))
        self.Customers.grid(row=3, column=0)
        self.CustomersImage = PhotoImage(master=self, file='../Data/Resources/Main/Customers.png')
        self.Customers['image'] = self.CustomersImage

        self.Configuration = Button(self.Tools, command=lambda: Settings(self), width=11)
        self.Configuration.grid(row=4, column=0)
        self.ConfigurationImage = PhotoImage(master=self, file='../Data/Resources/Main/Configuration.png')
        self.Configuration['image'] = self.ConfigurationImage

        """Creates and packs a Frame widget using the grid geometry manager"""
        self.Background = Frame(self)
        self.Background.grid(row=0, column=1, rowspan=2, sticky=N + E + S + W)

        """Loads background image file, applies it onto a Label widget and packs it using the grid geometry manger"""
        self.BackgroundImage = PhotoImage(file='../Data/Resources/Main/Logo.png')
        self.BackgroundLabel = Label(self.Background, image=self.BackgroundImage)
        self.BackgroundLabel.grid(row=0, column=0)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)


"""The scope in which the interpreter’s main program executes"""
if __name__ == '__main__':
    """Creates instance of the MainMenu class"""
    MainMenu()
