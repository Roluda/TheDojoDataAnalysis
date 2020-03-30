import View
import Data
import MoveIncidentFilter as MIF



class Application:
    """the main class"""
    def __init__(self):
        print("initializing Application")
        self.name = "Nice App"
        self.mainWindow = View.MainWindow(self)
        self.mainWindow.window.mainloop()

    def initializeData(self, filepaths):
        self.data = Data.Data(filepaths)
        self.moveIncidentFilter = MIF.MoveIncidentFilter(self.data)
        self.mainWindow.activateModuleSelect()