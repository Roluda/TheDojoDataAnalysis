import matplotlib.pyplot as mpl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
import Controller as C

diagrams = {"Bar Diagram","Pie Diagram","Heatmap","Graph"}

class EmptyDiagramFrame(tk.Frame):
    def __init__(self, master=None, controller=None, onCreateDiagram = [lambda *args : None], cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.controller = controller
        self.newDiagramTkVar = tk.StringVar(self)
        self.newDiagramTkVar.set("Add Diagram..")
        self.newDiagramTkVar.trace('w', self._createNewDiagramCallback)
        self.newDiagramMenu = tk.OptionMenu(self, self.newDiagramTkVar, *diagrams)
        self.newDiagramMenu.grid()

    def _createNewDiagramCallback(self, *args):
        self.newDiagramMenu.grid_remove()
        self.label = tk.Label(self, text=self.newDiagramTkVar.get())
        self.label.grid(row = 0, column=0, sticky ="NW")
        self.removeButton = tk.Button(self, text="remove", command = self.destroy)
        self.removeButton.grid(row = 0, column = 1, sticky = "E")
        if self.newDiagramTkVar.get() == "Bar Diagram":
            self.diagramFrame = BarDiagramFrame(self, data = self.controller.filterOutlet.output())
        else:
            self.diagramFrame = Frame(self)
        self.diagramFrame.grid(sticky="SE")

class BarDiagramFrame(tk.Frame):
    def __init__(self, master=None, data = None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.data = data

        self.attributeTkVar = tk.StringVar(self)
        self.attributeTkVar.set("Choose Attribut")
        self.attributeTkVar.trace('w', self.draw)
        self.attributeSelect = tk.OptionMenu(self, self.attributeTkVar, C.uniqueAttributesInData(self.data))
        self.attributeSelect.grid(row = 2, sticky="S")

        self.draw(data)

    def draw(self, data):
        print("drawing")
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, sticky="NE")

        toolbarFrame = tk.Frame(self)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()
        toolbarFrame.grid()
        canvas.get_tk_widget().grid(row=1, sticky="NE")
        pass

def displayTotalMoves(dictionary):
    x = np.arange(len(dictionary))
    width = 0.35

    fig, ax = mpl.subplots()
    rects = ax.bar(x, dictionary.values(), width, label = dictionary.keys())
    ax.set_ylabel('Amount')
    ax.set_title('Moves used in Data')
    ax.set_xticks(x)
    ax.set_xticklabels(dictionary.keys(), rotation=35, ha ="right")

    fig.tight_layout()
    mpl.show()


