import tkinter as tk
import Filters as F
import View

presets={

    "Name Filter": lambda : F.WhitelistFilter("name"),
    "Entity Name Filter": lambda : F.WhitelistFilterChild("entity", "name"),
    "Room Name Filter": lambda : F.WhitelistFilterChild("entity", "currentRoom"),

}

class EmptyFilterFrame(tk.Frame):
    def __init__(self, master, onFilterSelect = [lambda filter : None], cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.onFilterSelect = onFilterSelect

        self.newFilterTkVar = tk.StringVar(self)
        self.newFilterTkVar.set("Add Filter..")
        self.filters = presets.keys()
        self.newFilterTkVar.trace('w', self._createNewFilterCallback)
        self.newFilterMenu = tk.OptionMenu(self, self.newFilterTkVar, *self.filters)
        self.newFilterMenu.pack(anchor="s")
       
    def _createNewFilterCallback(self, *args):
        self.newFilterMenu.pack_forget()
        self.filter = presets[self.newFilterTkVar.get()]()
        for action in self.onFilterSelect: action(self.filter)

        self.headFrame = tk.Frame(self)
        self.headFrame.pack(anchor="n", expand=True, fill=tk.X)
        self.label = tk.Label(self.headFrame, text=self.newFilterTkVar.get())
        self.label.pack(anchor="w")
        self.removeButton = tk.Button(self.headFrame, text="remove", command = self.destroy)
        self.removeButton.pack(anchor="e")

        if isinstance(self.filter, F.WhitelistFilterChild):
            self.settingFrame =CheckboxFilterFrame(
                self,
                self.filter.potentialSet(), 
                update=lambda: self.filter.assignWhitelist(self.settingFrame.checkedOptions())
            )
        elif isinstance(self.filter, F.Filter):
            self.settingFrame=CheckboxFilterFrame(
                self,
                self.filter.potentialSet(), 
                update=lambda: self.filter.assignWhitelist(self.settingFrame.checkedOptions())
            )
        elif isinstance(self.filter, F.Filter):
            self.settingFrame=tk.Frame(self)
        self.settingFrame.pack(expand= True, fill=tk.X, anchor="s")



    def destroy(self):
        if hasattr(self, "filter"):
            self.filter.delete()
        super().destroy()

class CheckboxFilterFrame(tk.Frame):
    """creates a frame containing a set of otions

    get checkedOptions for a set of selected otions"""
    def __init__(self, master, options, update = lambda *args : None):
        super().__init__(master)
        self.update = update
        self.checkedTkVariable = {}
        for (index, option) in enumerate(options):
            boolVar = tk.Variable(self)
            boolVar.set(False)
            boolVar.trace('w', self.updatedOptions)
            self.checkedTkVariable[option] = boolVar
            checkBox = tk.Checkbutton(self, text=option, variable=boolVar)
            checkBox.grid(sticky="W")

    def updatedOptions(self, *args):
        self.update()

    def checkedOptions(self):
        newSet=set()
        for (option, value) in self.checkedTkVariable.items():
            newSet.add(option) if value.get() else None
        return newSet

