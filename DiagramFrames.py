import matplotlib.pyplot as mpl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
import Controller as C

diagrams = {"Bar Diagram","Scatter Diagram"}

class EmptyDiagramFrame(tk.Frame):
    def __init__(self, master=None, controller=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.controller = controller
        self.onRefresh = []
        self.onCreateDiagram = []

        self.newDiagramTkVar = tk.StringVar(self)
        self.newDiagramTkVar.set("Add Diagram..")
        self.newDiagramTkVar.trace('w', self._createNewDiagramCallback)
        self.newDiagramMenu = tk.OptionMenu(self, self.newDiagramTkVar, *diagrams)
        self.newDiagramMenu.grid()

    def _createNewDiagramCallback(self, *args):
        self.newDiagramMenu.grid_remove()
        for action in self.onCreateDiagram: action()
        self.label = tk.Label(self, text=self.newDiagramTkVar.get())
        self.label.grid(row = 0, column=0, sticky ="NW")
        self.removeButton = tk.Button(self, text="remove", command = self.destroy)
        self.removeButton.grid(row = 0, column = 2, sticky = "E")
        self.refreshButton = tk.Button(self, text="refresh", command = self.refresh)
        self.refreshButton.grid(row=0, column = 1, sticky = "E")
        if self.newDiagramTkVar.get() == "Bar Diagram":
            self.diagramFrame = BarDiagramFrame(self, controller = self.controller)
            self.onRefresh.append(self.diagramFrame.refresh)
        elif self.newDiagramTkVar.get() == "Scatter Diagram":
            self.diagramFrame = ScatterDiagramFrame(self, controller = self.controller)
            self.onRefresh.append(self.diagramFrame.refresh)
        elif self.newDiagramTkVar.get() == "Pie Diagram":
            self.diagramFrame = PieDiagramFrame(self, controller=self.controller)
            self.onRefresh.append(self.diagramFrame.refresh)
        self.diagramFrame.grid(sticky="SE")

    def refresh(self):
        for action in self.onRefresh: action()


class BarDiagramFrame(tk.Frame):
    def __init__(self, master=None, controller = None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.controller = controller
        self.attributeSet = sorted(C.uniqueLanguageAttributesInData(self.controller.treeOutput()))
        self.attributeTkVar = tk.StringVar(self)
        self.attributeTkVar.set("select attribut")
        self.attributeTkVar.trace('w', self.refresh)
        self.attributeSelect = tk.OptionMenu(self, self.attributeTkVar, *self.attributeSet)
        self.attributeSelect.grid(row = 2, sticky="S")

        self.fig, self.ax = mpl.subplots()
        self.updateFigure()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, sticky="NE")
        self.toolbarFrame = tk.Frame(self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.update()
        self.toolbarFrame.grid()
        self.canvas.get_tk_widget().grid(row=1, sticky="NE")

    def refresh(self, *args):
        self.ax.clear()
        self.updateFigure()
        self.canvas.draw()

    def updateFigure(self):
        drawDict = {}
        try:
            for element in self.controller.treeOutput():
                flat = C.flatElement(element)
                if self.attributeTkVar.get() in flat.keys():
                    if flat[self.attributeTkVar.get()] not in drawDict.keys():
                        drawDict[flat[self.attributeTkVar.get()]] = 1
                    else:
                        drawDict[flat[self.attributeTkVar.get()]] += 1
            x = np.arange(len(drawDict))
            width=.35
            rects = self.ax.bar(x, drawDict.values(), width, label=drawDict.keys())
            self.ax.set_ylabel("Oilcatz rules")
            self.ax.set_title("total of "+self.controller.root.tag)
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(drawDict.keys(), rotation=35, ha ="right")
            self.fig.tight_layout()
        except:
            pass



class ScatterDiagramFrame(tk.Frame):
    def __init__(self, master=None, controller = None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.controller = controller
        self.attributeSet = sorted(C.uniqueNumAttributesInData(self.controller.treeOutput()))

        self.settingParent = tk.Frame(self)

        self.attributeXTkVar = tk.StringVar(self)
        self.attributeXTkVar.set("select attribut X")
        self.attributeXTkVar.trace('w', self.refresh)
        self.attributeXSelect = tk.OptionMenu(self.settingParent, self.attributeXTkVar, *self.attributeSet)
        self.attributeXSelect.grid(row = 0, column =0, sticky="S")


        self.attributeYTkVar = tk.StringVar(self)
        self.attributeYTkVar.set("select attribut Y")
        self.attributeYTkVar.trace('w', self.refresh)
        self.attributeYSelect = tk.OptionMenu(self.settingParent, self.attributeYTkVar, *self.attributeSet)
        self.attributeYSelect.grid(row = 0, column =1, sticky="W")
        self.settingParent.grid(row=2, column=0, sticky="S")

        self.fig, self.ax = mpl.subplots()
        self.updateFigure()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, sticky="NE")
        self.toolbarFrame = tk.Frame(self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.update()
        self.toolbarFrame.grid()
        self.canvas.get_tk_widget().grid(row=1, sticky="NE")

    def refresh(self, *args):
        self.ax.clear()
        self.updateFigure()
        self.canvas.draw()

    def updateFigure(self):
        try:
            pointsX=[]
            pointsY=[]
            for element in self.controller.treeOutput():
                flat = C.flatElement(element)
                pointsX.append(float(flat[self.attributeXTkVar.get()]))
                pointsY.append(float(flat[self.attributeYTkVar.get()]))
            self.ax.scatter(pointsX, pointsY, color='b', s=1)
            self.ax.set_xlabel(self.attributeXTkVar.get())
            self.ax.set_ylabel(self.attributeYTkVar.get())
            self.ax.set_title(self.controller.root.tag)
            self.ax.set_title("values of "+self.controller.filterOutlet.root.tag)
            #self.ax.set_xticks(x)
            self.fig.tight_layout()
        except:
            pass


class PieDiagramFrame(tk.Frame):
    def __init__(self, master=None, controller = None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.controller = controller
        self.attributeSet = sorted(C.uniqueLanguageAttributesInData(self.controller.treeOutput()))
        self.attributeTkVar = tk.StringVar(self)
        self.attributeTkVar.set("select attribut")
        self.attributeTkVar.trace('w', self.refresh)
        self.attributeSelect = tk.OptionMenu(self, self.attributeTkVar, *self.attributeSet)
        self.attributeSelect.grid(row = 2, sticky="S")

        self.fig, self.ax = mpl.subplots()
        self.updateFigure()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, sticky="NE")
        self.toolbarFrame = tk.Frame(self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.update()
        self.toolbarFrame.grid()
        self.canvas.get_tk_widget().grid(row=1, sticky="NE")

    def refresh(self, *args):
        self.ax.clear()
        self.updateFigure()
        self.canvas.draw()

    def updateFigure(self):
        drawDict = {}
        try:
            for element in self.controller.treeOutput():
                flat = C.flatElement(element)
                sum = len(self.controller.treeOutput())
                if self.attributeTkVar.get() in flat.keys():
                    if flat[self.attributeTkVar.get()] not in drawDict.keys():
                        drawDict[flat[self.attributeTkVar.get()]] = 1
                    else:
                        drawDict[flat[self.attributeTkVar.get()]] += 1

            self.ax.autoscale(True)
            self.ax.pie(drawDict.values(), labels=drawDict.keys(), autopct="%1.1%%")

            #self.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            self.ax.set_title("relatives of "+self.controller.root.tag)
            #self.fig.tight_layout()

        except:
            pass