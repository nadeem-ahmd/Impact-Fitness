import configparser
from tkinter import *
from tkinter import filedialog as dialog
from tkinter import messagebox as message
from tkinter.ttk import *

from src.utils import *

try:
    import pymysql

    remoteAvailable = True
except ImportError:
    remoteAvailable = False


class Connect():
    """Creates an connection to get and set application settings"""

    def __init__(self, File='../Data/Configuration.ini'):
        """Establishes core configuration details and opens configuration file"""

        self.File = File
        self.Config = configparser.ConfigParser()
        self.Config.read(self.File)

    def GetValue(self, Section, Field):
        """Returns a specific field from the configuration file using the parameters"""

        return self.Config.get(Section, Field)

    def SetValue(self, Section, Field, Value):
        """Sets a specific field in the configuration file to a value specified in the parameter"""

        self.Config.set(Section, Field, Value)

        """Opens the configuration file with the write setting to replace contents"""
        with open(self.File, 'w') as ConfigFile:
            """Will write all of the configuration into the opened file"""
            self.Config.write(ConfigFile)


class Settings(Toplevel):
    """Creates an instance of the InventoryManager interface as a subclass of the TopLevel Frame widget"""

    def __init__(self, *args, **kwargs):
        """Initialises the different features for the application"""

        """Setting the master class as the argument passed when the class was called, will be Main Menu root instance"""
        self.master = args[0]

        """Parameters are passed onto the Tkinter parent Toplevel class"""
        super().__init__(**kwargs)

        """Sets application title"""
        self.title('Settings')

        """Calls class defined functions to set up the interface and load saved configuration"""
        self.LoadInterface()
        self.LoadConfiguration()

        """Disables the ability for window resizing"""
        self.resizable(0, 0)

        """Starts the main loop for the application"""
        self.mainloop()

    def LoadInterface(self):
        """Called to set up the core interface widgets for the application"""

        """Creates and packs the Frame widget onto the root interface using the pack geometry manager"""
        self.MainFrame = Frame(self)
        self.MainFrame.pack(fill=BOTH)

        """Creates and packs the LabelFrame widget onto the MainFrame frame using the pack geometry manager"""
        self.DatabaseFrame = LabelFrame(self.MainFrame, text='Database')
        self.DatabaseFrame.pack(fill=BOTH, side=LEFT, padx=5, pady=5)

        """Creates and packs Radiobutton widgets onto the DatabaseFrame using DatabaseChoice var"""
        self.DatabaseChoice = StringVar()
        self.Text = Radiobutton(self.DatabaseFrame, text='Text', command=self.SelectDatabase)
        self.Text.config(variable=self.DatabaseChoice, value='Text', )
        self.Text.pack(anchor=W)
        self.Local = Radiobutton(self.DatabaseFrame, text='Local', command=self.SelectDatabase)
        self.Local.config(variable=self.DatabaseChoice, value='Local')
        self.Local.pack(anchor=W)

        """Creates and packs the Frame widget onto the DatabaseFrame widget using the pack geometry manager"""
        self.LocalConfig = Frame(self.DatabaseFrame)
        self.LocalConfig.pack()

        """Creates and packs the Frame widget onto the LocalConfig widget using the pack geometry manager"""
        self.LocalEntry = Entry(self.LocalConfig, width=30)
        self.LocalEntry.grid(row=0, column=0, padx=3)

        """Creates and packs Button widget onto LocalConfig frame so user can select local file"""
        self.LocalButton = Button(self.LocalConfig, text='...', command=self.SelectLocal, width=4)
        self.LocalButton.grid(row=0, column=1, padx=3)

        """Creates and packs Radiobutton widget onto the DatabaseFrame using DatabaseChoice var"""
        self.Remote = Radiobutton(self.DatabaseFrame, text='Remote', command=self.SelectDatabase)
        self.Remote.config(variable=self.DatabaseChoice, value='Remote')
        self.Remote.pack(anchor=W)

        """Creates and packs the Frame widget onto the DatabaseFrame widget using the pack geometry manager"""
        self.RemoteConfig = Frame(self.DatabaseFrame)
        self.RemoteConfig.pack()

        """Creates and packs the Label widgets onto the RemoteConfig frame using the grid geometry manager"""
        self.HostLabel = Label(self.RemoteConfig, text='Host:')
        self.HostLabel.grid(row=0, column=0, sticky=W, padx=10)
        self.UserLabel = Label(self.RemoteConfig, text='Username:')
        self.UserLabel.grid(row=2, column=0, sticky=W, padx=10)
        self.PassLabel = Label(self.RemoteConfig, text='Password:')
        self.PassLabel.grid(row=3, column=0, sticky=W, padx=10)

        """Creates and packs the Entry widgets onto the RemoteConfig frame using the grid geometry manager"""
        self.HostEntry = Entry(self.RemoteConfig, width=25)
        self.HostEntry.grid(row=0, column=1, padx=10, pady=5)
        self.UserEntry = Entry(self.RemoteConfig, width=25)
        self.UserEntry.grid(row=2, column=1, padx=10, pady=5)
        self.PassEntry = Entry(self.RemoteConfig, width=25)
        self.PassEntry.grid(row=3, column=1, padx=10, pady=5)

        """Creates and packs a Button onto the same frame using the grid geometry manager"""
        self.SaveButton = Button(self.RemoteConfig, text='Save', command=self.SaveConfiguration)
        self.SaveButton.grid(row=4, column=0, columnspan=2, pady=5)

        """Used to place the window at the center of the screen"""
        ConfigureInterface(self)

    def SelectDatabase(self):
        """Called when the OptionMenu selection is changed to update the configuration and/or change settings"""

        """For all database types, update the configuration fie to change the database type"""
        Connect().SetValue('DATABASE', 'TYPE', self.DatabaseChoice.get())

        """Will reload the the interface and configuration after settings have been changed"""
        self.LoadConfiguration()

    def SelectLocal(self, *Event):
        """Called when the LocalConfig button is pressed to allow local file selection"""

        try:

            """Asks user for the local file location using various parameter options"""
            File = dialog.askopenfile(mode='r+', title='Select database', defaultextension='.db', parent=self,
                                      filetypes=[('Local database', '.db')],
                                      initialfile=Connect().GetValue('LOCAL', 'PATH'))

            """Updates the configuration file setting to the local database"""
            Connect().SetValue('LOCAL', 'PATH', File.name)

            """Inserts the local database file name into the LocalEntry widget"""
            self.LocalEntry.delete(0, END)
            self.LocalEntry.insert(END, Connect().GetValue('LOCAL', 'PATH'))
        except AttributeError as E:

            """If an error occurs, then set the OptionMenu choice as the previous option and give error message"""
            self.DatabaseChoice.set(self.Type)
            message.showerror('Error', 'Error selecting file: ' + str(E), parent=self)
            return

    def SaveConfiguration(self):
        """Called when the save button is pressed to update the remote database attributes"""

        """If all of the entries have values, update the configuration file settings, otherwise give error message"""
        if self.HostEntry.get() and self.UserEntry.get() and self.PassEntry.get():
            Connect().SetValue('REMOTE', 'HOST', self.HostEntry.get())
            Connect().SetValue('REMOTE', 'USERNAME', self.UserEntry.get())
            Connect().SetValue('REMOTE', 'PASSWORD', self.PassEntry.get())
            message.showinfo('Success', 'Saved remote database configuration', parent=self)
        else:
            message.showerror('Error', 'Error whilst saving configuration, check entries', parent=self)

    def LoadConfiguration(self):
        """Called to update the interface to show existing configuration """

        """Creates separate lists for all the entries and labels on the interface"""
        self.Entries = [self.HostEntry, self.UserEntry, self.PassEntry]
        self.Labels = [self.HostLabel, self.UserLabel, self.PassLabel]

        """Loads the database type and remote database information from the configuration file"""
        self.Type = Connect().GetValue('DATABASE', 'TYPE')
        self.Data = [Connect().GetValue('REMOTE', 'HOST'),
                     Connect().GetValue('REMOTE', 'USERNAME'),
                     Connect().GetValue('REMOTE', 'PASSWORD')]

        """Sets the selected database type for the Radio options to the configuration database type"""
        self.DatabaseChoice.set(self.Type)

        """Inserts the local database file name into the LocalEntry widget"""
        self.LocalEntry.delete(0, END)
        self.LocalEntry.insert(END, Connect().GetValue('LOCAL', 'PATH'))

        """Loads entires with remote database details"""
        self.SaveButton['state'] = NORMAL
        for Entry in self.Entries:
            Entry.delete(0, END)
            Entry.insert(0, self.Data[self.Entries.index(Entry)])
            Entry['state'] = ACTIVE

        """If the selected option is not remote, disable the button, entry and label widgets"""
        if self.DatabaseChoice.get() != 'Remote':
            self.SaveButton['state'] = DISABLED
            for Entry in self.Entries:
                Entry['state'] = DISABLED
            for Label in self.Labels:
                Label['state'] = DISABLED

        """Sets the Local widgets as active or disabled depending on the chosen configuration"""
        if self.DatabaseChoice.get() == 'Local':
            self.LocalButton['state'] = ACTIVE
            self.LocalEntry['state'] = ACTIVE
        else:
            self.LocalButton['state'] = DISABLED
            self.LocalEntry['state'] = DISABLED

        if not remoteAvailable:
            self.Remote['state'] = DISABLED
