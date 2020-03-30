import Data
import xml.etree.ElementTree as ET

xmlns = {"namespace" : "http://schema.slothsoft.net/trialoftwo/database"}

class MoveIncidentFilter:
    """has multiple options to filter move incidents"""

    def __init__(self, data):
        self.movesRaw = data.database.findall(".//namespace:moveIncident", xmlns)
        self.movesFiltered = self.movesRaw

    def unfilter(self):
        self.movesFiltered = self.movesRaw

    def filterMovesByEntities(self, entities = None):
        """filters moves to only contain moves enacted by specified entities. No filter applied when passed 
        without any argument"""

        copy = self.movesFiltered
        for move in self.movesFiltered:
            if entities is not None and move.find("namespace:entity", xmlns).get("name") not in entities:
                copy.remove(move)

        self.movesFiltered = copy

    def filterMovesByRooms(self, rooms = None):
        """filters moves to only contain moves enacted in a specified room. No filter applied when passed
        without any argument"""

        copy = self.movesFiltered
        for move in self.movesFiltered:
            if rooms is not None and move.find("namespace:entity", xmlns).get("currentRoom") not in rooms:
                copy.remove(move)

        self.movesFiltered = copy

    def totalMovesFiltered(self):
        """sum of each individual move in the filtered data.

        return a dictionary"""

        dict = {}
        for move in self.movesFiltered:
            if move.get("name") not in dict.keys():
                dict[move.get("name")] = 1
            else:
                dict[move.get("name")] += 1

        return dict




