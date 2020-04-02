import tkinter as tk
from tkinter import filedialog
import FilterFrames as FF
import DiagramFrames as DF
import Filters
import Controller as C

font="Helvetica 12"
fontBold="Helvetica 12 bold"
datapoints = {"moveIncident", "deathIncident", "spawnIncident", "hurtIncident"}

class MainWindow(tk.Tk):
    """the main Window"""
    def __init__(self):
        super().__init__()
        self.title("Trial of Two player data Analysis tool")
        self.controller = C.FilterController()
        self.onDeleteFilters = []
        self.onDeleteDiagrams = []
        self.onUpdateDiagrams = []

        self.settingsParent = tk.Frame(self, width=400)
        self.settingsParent.grid(column=0, sticky="NW")
        self.importFrame = ImportFrame(self.settingsParent, self.importXmlCallback, relief ="raised", borderwidth =2)
        self.importFrame.pack(expand=True, anchor="n", fill=tk.X)
        
        self.mainloop()
   
    def importXmlCallback(self):
        for action in self.onDeleteFilters: action()
        for action in self.onDeleteDiagrams: action()
        self.controller.newData(self.importFrame.currentFilepath)
        if(hasattr(self, "dataSelectFrame")): self.dataSelectFrame.destroy()
        self.dataSelectFrame = DataSelectFrame(self.settingsParent, self.selectChangeCallback, relief ="raised", borderwidth =2)
        self.dataSelectFrame.pack(expand=True, anchor="n", fill=tk.X)
        
    def selectChangeCallback(self):
        for action in self.onDeleteFilters: action()
        for action in self.onDeleteDiagrams: action()
        self.controller.newFilterOutlet(tag = self.dataSelectFrame.dataSelectTkVar.get()),
        self.addEmptyFilterFrame()
        self.addEmptyDiagramFrame()
        
    def addEmptyFilterFrame(self, *args):
        newFrame = FF.EmptyFilterFrame(self.settingsParent, [self.addEmptyFilterFrame, self.controller.addFilter], relief = "raised", borderwidth=2)
        newFrame.pack(expand=True, anchor="n", fill=tk.X)
        self.onDeleteFilters.append(newFrame.destroy)

    def addEmptyDiagramFrame(self, *args):
        newDiagram = DF.EmptyDiagramFrame(self, controller=self.controller, relief ="raised", borderwidth=2)
        self.onDeleteDiagrams.append(newDiagram.destroy)
        newDiagram.grid(column=1, row=0, sticky="NE")

class ImportFrame(tk.Frame):
    def __init__(self, master=None, onImport=lambda *args : None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.onImort = onImport
        self.currentFilepath = ""
        self.importHead=tk.Label(self, text="select a .xml file")
        self.importHead.grid(sticky="N")
        self.importButton = tk.Button(self, text="open explorer..", command= self.importXMLFiles)
        self.importButton.grid(sticky="NW")
    
    def importXMLFiles(self):
        self.currentFilepath = filedialog.askopenfilename()
        self.onImort()

class DataSelectFrame(tk.Frame):
    def __init__(self, master=None, onSelectChange=lambda *args : None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.onSelectChange = onSelectChange
        self.dataSelectTkVar = tk.StringVar(self)
        self.dataSelectTkVar.set("Choose..")
        self.dataSelectTkVar.trace('w', self.changedSelectCallback)
        self.dataSelectHead = tk.Label(self, text="select data")
        self.dataSelectHead.pack(fill=tk.X)
        self.dataSelectMenu = tk.OptionMenu(self, self.dataSelectTkVar, *datapoints)
        self.dataSelectMenu.pack(fill=tk.X)

    def changedSelectCallback(self, *args):
        self.onSelectChange()