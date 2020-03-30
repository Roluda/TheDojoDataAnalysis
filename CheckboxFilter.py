import tkinter as tk

class CheckboxFilter(tk.Frame):
    """creates a frame containing a set of otions

    get checkedOptions for a set of selected otions"""
    def __init__(self, master, options, update = lambda *args : None, name="filterGroup"):
        super().__init__(master)
        self.update = update
        self.label=tk.Label(self, text=name)
        self.label.grid(sticky = "W")
        self.checkedTkVariable = {}
        for (index, option) in enumerate(options):
            boolVar = tk.Variable(self)
            boolVar.set(False)
            boolVar.trace('w', self.updatedOptions)
            self.checkedTkVariable[option] = boolVar
            checkBox = tk.Checkbutton(self, text=option, variable=boolVar)
            checkBox.grid(row=index+2, sticky="W")

    def updatedOptions(self, *args):
        self.update()

    def checkedOptions(self):
        newSet=set()
        for (option, value) in self.checkedTkVariable.items():
            newSet.add(option) if value.get() is True else None
        return newSet

