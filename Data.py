import xml.etree.ElementTree as et
from io import StringIO 

class Data:
    """an element tree of xml files"""
    def __init__(self):
        self.database = []
        self.addedFilepaths = set()

    def addData(self, filepath):
        if filepath not in self.addedFilepaths:
            newTree = et.iterparse(filepath)
            for _, el in newTree:
                _, _, el.tag = el.tag.rpartition('}')
            self.database.append(newTree.root)
            self.addedFilepaths.add(filepath)
            print("xml files loaded: ", len(self.database))


