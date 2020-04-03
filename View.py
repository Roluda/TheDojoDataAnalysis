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
        self.diagramParent= tk.Frame(self)
        self.diagramParent.grid(row= 0, column=1, sticky="NE")
        self.importFrame = ImportFrame(self.settingsParent, self.importXmlCallback, relief ="raised", borderwidth =2)
        self.importFrame.pack(expand=True, anchor="n", fill=tk.X)
        
        #self.debugButton = tk.Button(self.settingsParent, text="ping filter chain", command= lambda: self.controller.root.pingDown(0))
        #self.debugButton.pack()
        #self.debugButton2 = tk.Button(self.settingsParent, text="count chain output", command= lambda: print(len(self.controller.treeOutput())))
        #self.debugButton2.pack()
        self.mainloop()
   
    def importXmlCallback(self):
        for action in self.onDeleteFilters: action()
        for action in self.onDeleteDiagrams: action()
        self.controller.newData(self.importFrame.currentFilepath)
        if(hasattr(self, "dataSelectFrame")): self.dataSelectFrame.destroy()
        self.dataSelectFrame = DataSelectFrame(self.settingsParent, self.selectChangeCallback, relief ="raised", borderwidth =2)
        self.dataSelectFrame.pack(expand=True, anchor="n", fill=tk.X)
        
    def selectChangeCallback(self):
        self.deleteFilters()
        self.deleteDiagrams()
        self.controller.newFilterTree(tag = self.dataSelectFrame.dataSelectTkVar.get()),
        self.addEmptyFilterFrame()
        self.addEmptyDiagramFrame()
        
    def addEmptyFilterFrame(self, *args):
        print("addEmptyFilterFrame")
        newFrame = FF.EmptyFilterFrame(self.settingsParent,self.controller, relief = "raised", borderwidth=2)
        newFrame.pack(expand=True, anchor="n", fill=tk.X)
        newFrame.onFilterSelect.append(self.addEmptyFilterFrame)
        newFrame.onFilterUpdate.append(self.updateDiagrams)
        self.onDeleteFilters.append(newFrame.destroy)

    def addEmptyDiagramFrame(self, *args):
        newDiagram = DF.EmptyDiagramFrame(self.diagramParent, controller=self.controller, relief ="raised", borderwidth=2)
        newDiagram.onCreateDiagram.append(self.addEmptyDiagramFrame)
        self.onDeleteDiagrams.append(newDiagram.destroy)
        #self.onUpdateDiagrams.append(newDiagram.refresh)
        newDiagram.pack(expand=True, side=tk.LEFT, fill=tk.Y)

    def updateDiagrams(self, *args):
        for action in self.onUpdateDiagrams: action()

    def deleteFilters(self, *args):
        for action in self.onDeleteFilters: action()

    def deleteDiagrams(self, *args):
        for action in self.onDeleteDiagrams: action()


class ImportFrame(tk.Frame):
    def __init__(self, master=None, onImport=lambda *args : None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.onImort = onImport
        self.currentFilepath = ""
        self.importHead=tk.Label(self, text="select a .xml file")
        self.importHead.pack(fill=tk.X)
        self.importButton = tk.Button(self, text="open explorer..", command= self.importXMLFiles)
        self.importButton.pack(fill=tk.X)
    
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