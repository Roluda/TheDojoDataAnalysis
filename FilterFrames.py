import tkinter as tk
import Filters as F
import View

presets={

    "Name Filter": lambda : F.WhitelistFilter("name"),
    "Entity Name Filter": lambda : F.WhitelistFilterChild("entity", "name"),
    "Room Name Filter": lambda : F.WhitelistFilterChild("entity", "currentRoom"),

}

class EmptyFilterFrame(tk.Frame):
    def __init__(self, master, controller, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.controller = controller
        self.onFilterSelect = []
        self.onFilterUpdate = []

        self.newFilterTkVar = tk.StringVar(self)
        self.newFilterTkVar.set("Add Filter..")
        self.filters = presets.keys()
        self.newFilterTkVar.trace('w', self._createNewFilterCallback)
        self.newFilterMenu = tk.OptionMenu(self, self.newFilterTkVar, *self.filters)
        self.newFilterMenu.pack(anchor="s")
       
    def _createNewFilterCallback(self, *args):
        self.newFilterMenu.pack_forget()
        self.filter = presets[self.newFilterTkVar.get()]()
        self.controller.addFilter(self.filter)
        print("onFilterSelect: ",self.onFilterSelect)
        for action in self.onFilterSelect: action()

        self.label = tk.Label(self, text=self.newFilterTkVar.get())
        self.label.grid(row=0, column=0, sticky="NW")
        self.removeButton = tk.Button(self, text="remove", command = self.destroy)
        self.removeButton.grid(row=0, column=2, sticky="E")
        self.hideButton = tk.Button(self, text="hide", command = self.hide)
        self.hideButton.grid(row=0, column=1, sticky="E")

        if isinstance(self.filter, F.WhitelistFilterChild):
            self.settingFrame =CheckboxFilterFrame(
                self,
                self.filter.potentialSet(), 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignWhitelist(self.settingFrame.checkedOptions()))
        elif isinstance(self.filter, F.Filter):
            self.settingFrame=CheckboxFilterFrame(
                self,
                self.filter.potentialSet(), 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignWhitelist(self.settingFrame.checkedOptions()))
        elif isinstance(self.filter, F.Filter):
            self.settingFrame=tk.Frame(self)
        self.settingFrame.grid(sticky="E")

    def updatedFilterSettings(self):
        print("updateFilterSettings", "Delegate: ",self.onFilterUpdate)
        for action in self.onFilterUpdate: action()

    def destroy(self):
        if hasattr(self, "filter"):
            self.filter.delete()
        super().destroy()

    def hide(self):
        if self.settingFrame.winfo_ismapped:
            self.settingFrame.grid_remove()
        else:
            print("not mapped")
            seld.settingFrame.grid()

class CheckboxFilterFrame(tk.Frame):
    """creates a frame containing a set of otions

    get checkedOptions for a set of selected otions"""
    def __init__(self, master, options, update = [lambda *args : None]):
        super().__init__(master)
        self.update = update
        self.checkedTkVariable = {}
        for (index, option) in enumerate(options):
            boolVar = tk.BooleanVar(self)
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
            if value.get():
                newSet.add(option)
        return newSet
