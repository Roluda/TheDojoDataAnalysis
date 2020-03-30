import tkinter as tk
import MoveIncidentView as MIV
from tkinter import filedialog

font="Helvetica 12"
fontBold="Helvetica 12 bold"

class MainWindow:
    """the main Window"""
    def __init__(self, application):
        self.window = tk.Tk()
        self.window.title("Trial of Two player data Analysis tool")
        self.window.geometry("1200x800")
        self.application = application

        self.importHead=tk.Label(self.window, text="select a .xml file", font=fontBold)
        self.importHead.grid(sticky="NW")
        self.importButton = tk.Button(self.window, text="open explorer..", command= lambda: self.getXMLFiles())
        self.importButton.grid(sticky="NW")

    def getXMLFiles(self):
        self.window.withdraw()
        filepath= filedialog.askopenfilename()
        self.window.deiconify()
        self.application.initializeData(filepath)

    def activateModuleSelect(self):
        if hasattr(self, "modulesMenu"):
            return
        self.moduleTkVar = tk.StringVar(self.window, name="module")
        self.moduleTkVar.set("Choose..")
        self.modules = {"MoveIncidents", "DeathIncidents"}
        self.moduleTkVar.trace('w', self.changeModuleCallback)
        self.moduleHead = tk.Label(self.window, text="select datapoint", font = fontBold)
        self.moduleHead.grid(sticky="NW")
        self.modulesMenu = tk.OptionMenu(self.window, self.moduleTkVar, *self.modules)
        self.modulesMenu.grid(sticky="NW")
        
        self.moveIncidentFilterFrame = MIV.MoveIncidentFilterFrame(self.window, self.application)
        self.moveIncidentFilterFrame.grid()
        self.moveIncidentFilterFrame.grid_remove()

        self.deathIncidentFilterFrame = tk.Frame(self.window)
        self.deathIncidentFilterFrame.grid()
        self.moveIncidentFilterFrame.grid_remove()

    def changeModuleCallback(self, *args):
        self.deathIncidentFilterFrame.grid_remove()
        self.moveIncidentFilterFrame.grid_remove()
        if self.moduleTkVar.get() == "MoveIncidents":
            self.moveIncidentFilterFrame.grid()
            self.moveIncidentFilterFrame.updateFilterCallback()

        elif self.moduleTkVar.get() == "DeathIncidents":
            self.deathIncidentFilterFrame.grid()

    def changeDataCallback(self):
        self.moveIncidentFilterFrame.updateFilterCallback()




        





