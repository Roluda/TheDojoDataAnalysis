import Data
import xml.etree.ElementTree

class Filter:
    """a filter takes a list of elementTree elements outputs them

    inherit this class and override the output to add new filters
    
    filters can be chained together by setting a parent 
    
    the root filter will return 'data'"""
    def __init__(self, parent = None, data = None):
        self.parent = parent
        self.child = None
        self.root = self
        self.data = data
        if self.parent is not None:
            parent.attach(self)

    def attach(self, filter):
        """adds the filter as child, previous child will be attached to new child"""
        print("attaching: ", filter, " to ", self)
        if self.child is not None:
            self.child.parent = filter
        self.child=filter
        filter.parent = self
        filter.root =  self.root
        
    def delete(self):
        if self.parent is not None:
            self.parent.child = self.child
        if self.child is not None:
            self.child.parent = self.parent

    def output(self):
        print("filter: ", self, " parent: ", self.parent)
        self.data = self.parent.output() if self.parent is not None else self.data
        return self.data


class TagFilter(Filter):
    """outputs all child elements with a tag
    """
    def __init__(self, tag, parent=None, data=None):
        super().__init__(parent=parent, data=data)
        self.tag = tag

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data        
        elements=[]
        for element in self.data:
            elements += element.findall(".//"+self.tag)
        return elements


class WhitelistFilterChild(Filter):
    """removes all elements without a "tag" child with "attribute" which value is not 
    contained by "whitelist"
    """
    def __init__(self, tag, attribute, whitelist = set(""), parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.tag = tag
        self.attribute = attribute
        self.whitelist = whitelist

    def assignWhitelist(self, whitelist):
        self.whitelist = whitelist

    def potentialSet(self):
        """returns a set of strings that could effectively be used for filtering"""
        whiteSet = set()
        for element in self.root.output():
            for candidate in element.findall(".//"+self.tag):
                whiteSet.add(candidate.get(self.attribute))
        return whiteSet

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = element.find(self.tag).get(self.attribute)
            if value is not None and value in self.whitelist:
                elements.append(element)
        return elements

class WhitelistFilter(Filter):
    """removes all elements without a with "attribute" which value is not 
    contained by "whitelist"
    """
    def __init__(self, attribute, whitelist = set(""), parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.attribute = attribute
        self.whitelist = whitelist

    def assignWhitelist(self, whitelist):
        self.whitelist = whitelist

    def potentialSet(self):
        """returns a set of strings that could effectively be used for filtering"""
        whiteSet = set()
        for candidate in self.root.output():
            whiteSet.add(candidate.get(self.attribute))
        return whiteSet

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = element.get(self.attribute)
            if value is not None and value in self.whitelist:
                elements.append(element)
        return elements