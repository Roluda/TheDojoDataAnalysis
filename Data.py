import xml.etree.ElementTree as et
from io import StringIO 

class Data:
    """an element tree of valid xml files"""
    def __init__(self):
        self.database = []

    def addData(self, filepath):
        newTree = et.iterparse(filepath)
        for _, el in newTree:
            _, _, el.tag = el.tag.rpartition('}')
        self.database.append(newTree.root)


