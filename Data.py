import xml.etree.ElementTree as et

ns = {"ns" : "http://schema.slothsoft.net/trialoftwo/database"}

class Data:
    """an element tree of valid xml files"""

    def __init__(self, filepath):
        self.tree = et.parse(filepath)
        self.database = self.tree.getroot()

    def getIndividualEntityNames(self):
        """returns a set of entity names in the data"""
        entities = set()
        for entity in self.database.findall(".//ns:entity", ns):
            entities.add(entity.get("name"))

        return entities

    def getIndividualRoomNames(self):
        """returns a set of entity names in the data"""
        rooms = set()
        for room in self.database.findall(".//ns:room", ns):
            rooms.add(room.get("name"))

        return rooms



