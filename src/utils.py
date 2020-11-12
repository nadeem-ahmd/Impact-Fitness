from tkinter import PhotoImage


def ConfigureInterface(Root):
    """Called to configure different parts of the interface such as the location, size and icon"""

    """Updates the Tk idletasks which sets the new required screen height and width of the application"""
    Root.update_idletasks()

    """Gathers the width and height of the screen the application is being run on"""
    ScreenWidth = Root.winfo_screenwidth()
    ScreenHeight = Root.winfo_screenheight()

    """Calculates the x and y coordinates to locate the center of the screen"""
    X = (ScreenWidth / 2) - (Root.winfo_reqwidth() / 2)
    Y = (ScreenHeight / 2) - (Root.winfo_reqheight() / 2)

    """Sets the application required width and height as well as the calculated  coordinates which will be the center"""
    Root.geometry('%dx%d+%d+%d' % (Root.winfo_reqwidth(), Root.winfo_reqheight(), X, Y))

    """Called to lift the new interface instance in front of the main menu by force focusing view on application"""
    Root.focus_force()

    """Sets the application icon"""
    Root.tk.call('wm', 'iconphoto', Root._w, PhotoImage(file='../Data/Resources/Icon.png'))

    """Setting the minimum application size as the required size"""
    Root.minsize(Root.winfo_width(), Root.winfo_height())


def SortData(Data):
    Sorted = False
    while not Sorted:
        Sorted = True
        for Sort in range(0, len(Data) - 1):
            if str(Data[Sort][1]) > str(Data[Sort + 1][1]):
                Sorted = False
                TempStore = Data[Sort + 1]
                Data[Sort + 1] = Data[Sort]
                Data[Sort] = TempStore
    return Data


def SortTree(Event, Treeview, Data):
    """Called from each separate after establishing header has been clicked"""

    """Checks which index needs sorting by checking the Treeview headers"""
    Index = int(Treeview.identify_column(Event.x)[1:]) - 1

    """Fills empty array with item ID's and item attributes to sort based on Index """
    UnsortedData = []
    for x in Treeview.get_children():
        Values = Treeview.item(x)['values']
        UnsortedData.append([int(Values[0]), Values[Index]])

    """Calls SortData function to carry out relevant sort algorithm on data"""
    UnsortedData = SortData(UnsortedData)

    """Finalises sorting by returning the data in order with original attributes"""
    SortedData = []
    for Sort in UnsortedData:
        for DataItem in Data:
            if int(Sort[0]) == int(DataItem.GetID()):
                SortedData.append(DataItem)
    return SortedData
