import tkinter as tk
import Filters as F
import View
import datetime

class EmptyFilterFrame(tk.Frame):
    def __init__(self, master, controller, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.controller = controller
        self.onFilterSelect = []
        self.onFilterUpdate = []
        self.onFrameDestroy = []

        self.newFilterTkVar = tk.StringVar(self)
        self.newFilterTkVar.set("Add Filter..")
        self.filters = sorted(self.controller.possibleFilters.keys())
        self.newFilterTkVar.trace('w', self._createNewFilterCallback)
        self.newFilterMenu = tk.OptionMenu(self, self.newFilterTkVar, *self.filters)
        self.newFilterMenu.pack(anchor="s")
       
    def _createNewFilterCallback(self, *args):
        self.newFilterMenu.pack_forget()
        self.filter = self.controller.possibleFilters[self.newFilterTkVar.get()]
        self.controller.addFilter(self.filter)
        print("onFilterSelect: ",self.onFilterSelect)
        for action in self.onFilterSelect: action()

        self.label = tk.Label(self, text=self.newFilterTkVar.get())
        self.label.grid(row=0, column=0, sticky="NW")
        self.removeButton = tk.Button(self, text="remove", command = self.destroy)
        self.removeButton.grid(row=0, column=2, sticky="E")
        self.hideButton = tk.Button(self, text="hide", command = self.hide)
        self.hideButton.grid(row=0, column=1, sticky="E")

        if isinstance(self.filter, F.WhitelistFilter):
            self.settingFrame =CheckboxFilterFrame(
                self,
                self.filter.potentialSet(), 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignWhitelist(self.settingFrame.checkedOptions()))
        elif isinstance(self.filter, F.WhitelistFilterChild):
            self.settingFrame=CheckboxFilterFrame(
                self,
                self.filter.potentialSet(), 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignWhitelist(self.settingFrame.checkedOptions()))
        elif isinstance(self.filter, F.RangeFilter):
            self.settingFrame=MinMaxFilterFrame(
                self,
                *self.filter.potentialRange(),
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignRange(*self.settingFrame.range()))
        elif isinstance(self.filter, F.RangeFilterChild):
            self.settingFrame=MinMaxFilterFrame(
                self,
                *self.filter.potentialRange(),
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignRange(*self.settingFrame.range()))
        elif isinstance(self.filter, F.BoolFilter):
            self.settingFrame=BoolFilterFrame(
                self,
                self.filter.attribute, 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignBool(self.settingFrame.checkedBool()))
        elif isinstance(self.filter, F.BoolFilterChild):
            self.settingFrame=BoolFilterFrame(
                self,
                self.filter.attribute, 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignBool(self.settingFrame.checkedBool()))
        elif isinstance(self.filter, F.DateFilter):
            self.settingFrame=DateFilterFrame(
                self,
                self.filter.potentialDates(), 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignDate(self.settingFrame.selectedDate()))
        elif isinstance(self.filter, F.DateFilterChild):
            self.settingFrame=DateFilterFrame(
                self,
                self.filter.potentialDates(), 
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignDate(self.settingFrame.selectedDate()))
        elif isinstance(self.filter, F.TimeFilter):
            self.settingFrame=TimeFilterFrame(
                self,
                *self.filter.potentialRange(),
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignRange(*self.settingFrame.timeRange()))
        elif isinstance(self.filter, F.TimeFilterChild):
            self.settingFrame=TimeFilterFrame(
                self,
                *self.filter.potentialRange(),
                update= lambda: self.updatedFilterSettings()
            )
            self.onFilterUpdate.append(lambda : self.filter.assignRange(*self.settingFrame.timeRange()))

        self.settingFrame.grid(sticky="E")

    def updatedFilterSettings(self):
        for action in self.onFilterUpdate: action()

    def destroy(self):
        for action in self.onFrameDestroy: action()
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

class MinMaxFilterFrame(tk.Frame):
    """creates a frame containing a min and a max slider

    get range for a set of selected otions"""
    def __init__(self, master, min, max, update = [lambda *args : None]):
        super().__init__(master)
        self.update = update
        self.resolution = (max-min)/250
        self.minTkVar = tk.DoubleVar(self)
        self.minTkVar.trace('w', self.updatedOptions)
        self.minTkVar.set(min)
        self.minSlider = tk.Scale(self, from_=min, to=max, variable = self.minTkVar, orient = tk.HORIZONTAL, label="min", length=250, resolution=self.resolution)
        self.minSlider.grid(row=0)

        self.maxTkVar = tk.DoubleVar(self)
        self.maxTkVar.trace('w', self.updatedOptions)
        self.maxTkVar.set(max)
        self.maxSlider = tk.Scale(self, from_=min, to=max, variable = self.maxTkVar, orient = tk.HORIZONTAL, label="max", length=250, resolution=self.resolution)
        self.maxSlider.grid(row=1)

        self.updatedOptions()

    def updatedOptions(self, *args):
        self.update()

    def range(self):
        return (self.minTkVar.get(), self.maxTkVar.get())

class BoolFilterFrame(tk.Frame):
    """creates a frame containing a set of otions

    get checkedOptions for a set of selected otions"""
    def __init__(self, master, attribute, update = [lambda *args : None]):
        super().__init__(master)

        self.update = update
        self.checkTkVar = tk.BooleanVar(self)
        self.checkTkVar.set(False)
        self.checkTkVar.trace('w', self.updatedOptions)
        self.check = tk.Checkbutton(self, text=attribute, variable = self.checkTkVar)
        self.check.grid(sticky='W')

        self.updatedOptions()

    def updatedOptions(self, *args):
        self.update()

    def checkedBool(self):
        return self.checkTkVar.get()

class DateFilterFrame(tk.Frame):
    def __init__(self, master, dates=set(), update = [lambda *args : None]):
        super().__init__(master)
        self.update = update

        self.label = tk.Label(self, text="select date")
        self.label.grid()

        self.dateSelect = tk.Listbox(self, selectmode=tk.SINGLE)
        for date in dates:
            self.dateSelect.insert(tk.END, date.isoformat())
        self.dateSelect.bind('<<ListboxSelect>>', self.updatedOptions)
        self.dateSelect.bind("<Button-1>", self.clickCallback)
        self.dateSelect.grid()

    def clickCallback(self, evt):
        self.dateSelect.selection_clear(0, self.dateSelect.size()-1)

    def selectedDate(self):
        index = self.dateSelect.curselection()[0]
        return datetime.date.fromisoformat(self.dateSelect.get(index))

    def updatedOptions(self, *args):
        self.update()

class TimeFilterFrame(tk.Frame):
    def __init__(self, master, min, max, update = [lambda *args : None]):
        super().__init__(master)
        self.update = update

        self.fromHourTkVar = tk.IntVar(self)
        self.fromHourTkVar.trace("w", self.updatedOptions)
        self.fromHourTkVar.set(min.hour)
        self.fromMinuteTkVar = tk.IntVar(self)
        self.fromMinuteTkVar.trace("w", self.updatedOptions)
        self.fromMinuteTkVar.set(min.minute)
        self.fromSecondTkVar = tk.IntVar(self)
        self.fromSecondTkVar.trace("w", self.updatedOptions)
        self.fromSecondTkVar.set(min.second)
        self.fromMicrosecondTkVar = tk.IntVar(self)
        self.fromMicrosecondTkVar.trace("w", self.updatedOptions)
        self.fromMicrosecondTkVar.set(min.microsecond)

        self.toHourTkVar = tk.IntVar(self)
        self.toHourTkVar.trace("w", self.updatedOptions)
        self.toHourTkVar.set(max.hour)
        self.toMinuteTkVar = tk.IntVar(self)
        self.toMinuteTkVar.trace("w", self.updatedOptions)
        self.toMinuteTkVar.set(max.minute)
        self.toSecondTkVar = tk.IntVar(self)
        self.toSecondTkVar.trace("w", self.updatedOptions)
        self.toSecondTkVar.set(max.second)
        self.toMicrosecondTkVar = tk.IntVar(self)
        self.toMicrosecondTkVar.trace("w", self.updatedOptions)
        self.toMicrosecondTkVar.set(max.microsecond)

        self.fromHourWheel = tk.Scale(self, from_=0, to=23, variable=self.fromHourTkVar, orient=tk.HORIZONTAL, label="Hour")
        self.fromMinuteWheel = tk.Scale(self, from_=0, to=59, variable=self.fromMinuteTkVar, orient=tk.HORIZONTAL, label="Min")
        self.fromSecondWheel = tk.Scale(self, from_=0, to=59, variable=self.fromSecondTkVar, orient=tk.HORIZONTAL, label="Sec")
        self.fromMicrosecondWheel = tk.Scale(self, from_=0, to=999999, variable=self.fromMicrosecondTkVar, orient=tk.HORIZONTAL, label="MicroS")
        self.toHourWheel = tk.Scale(self, from_=0, to=23, variable=self.toHourTkVar, orient=tk.HORIZONTAL, label="Hour")
        self.toMinuteWheel = tk.Scale(self, from_=0, to=59, variable=self.toMinuteTkVar, orient=tk.HORIZONTAL, label="Min")
        self.toSecondWheel = tk.Scale(self, from_=0, to=59, variable=self.toSecondTkVar, orient=tk.HORIZONTAL, label="Sec")
        self.toMicrosecondWheel = tk.Scale(self, from_=0, to=999999, variable=self.toMicrosecondTkVar, orient=tk.HORIZONTAL, label="MicroS")

        self.fromLabel= tk.Label(self, text="from")
        self.toLabel=tk.Label(self, text="to")
        self.fromLabel.grid(row=0, column=0, sticky="W")
        self.fromHourWheel.grid(row=1, column=0)
        self.fromMinuteWheel.grid(row=1, column=1)
        self.fromSecondWheel.grid(row=1, column=2)
        self.fromMicrosecondWheel.grid(row=1, column=3)
        self.toLabel.grid(row=2, column=0, sticky="W")
        self.toHourWheel.grid(row=3, column=0)
        self.toMinuteWheel.grid(row=3, column=1)
        self.toSecondWheel.grid(row=3, column=2)
        self.toMicrosecondWheel.grid(row=3, column=3)
        
    def timeRange(self):
        min = datetime.time(self.fromHourTkVar.get(), self.fromMinuteTkVar.get(), self.fromSecondTkVar.get(), self.fromMicrosecondTkVar.get())
        max = datetime.time(self.toHourTkVar.get(), self.toMinuteTkVar.get(), self.toSecondTkVar.get(), self.toMicrosecondTkVar.get())
        return (min, max)

    def updatedOptions(self, *args):
        self.update()