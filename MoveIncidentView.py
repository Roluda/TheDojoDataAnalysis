import tkinter as tk
import MoveIncidentFilter as MIF
import Application as App
import View
import CheckboxFilter as CF

class MoveIncidentFilterFrame(tk.Frame):
    """A frame containing all availiabe filter options"""

    def __init__(self, master, application):
        super().__init__(master)

        self.moveIncidentFilter = application.moveIncidentFilter

        self.head = tk.Label(self, text="select filters", font= View.fontBold)
        self.head.grid(row=0, sticky="W")

        self.entities = CF.CheckboxFilter(self, application.data.getIndividualEntityNames(), update= lambda: self.updateFilterCallback(), name="Filter Entities")
        self.entities.grid(row=2,sticky="NW")

        self.rooms = CF.CheckboxFilter(self, application.data.getIndividualRoomNames(), update= lambda: self.updateFilterCallback(), name="Filter Rooms")
        self.rooms.grid(row=2,column = 1, sticky="NW")

    def updateFilterCallback(self):
        self.moveIncidentFilter.unfilter()
        self.moveIncidentFilter.filterMovesByEntities(self.entities.checkedOptions())
        self.moveIncidentFilter.filterMovesByRooms(self.rooms.checkedOptions())





