import Data
import xml.etree.ElementTree
import datetime
import dateutil

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
        self.parent = None
        self.child = None

    def getRoot(self):
        if self.parent is None:
            return self
        else:
            return self.parent.getRoot()

    def getLeaf(self):
        if self.child is None:
            return self
        else:
            return self.child.getLeaf()

    def pingUp(self, inc):
        print(inc, self)
        if self.parent is not None:
            self.parent.pingUp(inc +1)

    def pingDown(self, inc):
        print(inc, self)
        if self.child is not None:
            self.child.pingDown(inc +1)

    def output(self):
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
            for candidate in element.iter(self.tag):
                whiteSet.add(candidate.get(self.attribute))
        return whiteSet

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = element.find(".//"+self.tag).get(self.attribute)
            if value is not None and value in self.whitelist:
                elements.append(element)
        return elements

class BoolFilter(Filter):
    """removes all elements without a with "attribute" which value is not 
    the same as this ones by "whitelist"
    """
    def __init__(self, attribute, bool = True, parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.attribute = attribute
        self.bool = bool

    def assignBool(self, bool):
        self.bool = bool

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = element.get(self.attribute)
            if self.bool and value in ["True", "true", "TRUE"]:
                elements.append(element)
            elif not self.bool and value in ["fasle", "False", "FALSE"]:
                elements.append(element)
        return elements

class BoolFilterChild(Filter):
    """removes all elements without a "tag" child with "attribute" which value is not 
    the same as this bool"
    """
    def __init__(self, tag, attribute, bool=False, parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.tag = tag
        self.attribute = attribute
        self.bool = bool

    def assignBool(self, bool):
        self.bool = bool

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = element.find(".//"+self.tag).get(self.attribute)
            if self.bool and value in ["True", "true", "TRUE"]:
                elements.append(element)
            elif not self.bool and value in ["false", "False", "FALSE"]:
                elements.append(element)
        return elements

class RangeFilter(Filter):
    """removes all elements without "attribute" which value is not 
    inside Range
    """
    def __init__(self, attribute, min =0, max=0, parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.attribute = attribute
        self.mini = min
        self.maxi = max

    def assignRange(self, min, max):
        self.mini = min
        self.maxi = max

    def potentialRange(self):
        """returns a min, max tupel that could be used for filtering"""
        values = []
        for candidate in self.root.output():
            values.append(float(candidate.get(self.attribute)))
        return (min(values), max(values))

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = float(element.get(self.attribute))
            if value >= self.mini and value <= self.maxi:
                elements.append(element)
        return elements

class RangeFilterChild(Filter):
    """removes all elements without a "tag" child with "attribute" which value is not 
    inside min max range
    """
    def __init__(self, tag, attribute, min=0, max=0, parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.tag = tag
        self.attribute = attribute
        self.min = min
        self.max = max

    def assignRange(self, min, max):
        self.min = min
        self.max = max

    def potentialRange(self):
        """returns a min, max tupel that could be used for filtering"""
        values = []
        for element in self.root.output():
            for candidate in element.iter(self.tag):
                values.append(float(candidate.get(self.attribute)))
        return (min(values), max(values))

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = float(element.find(".//"+self.tag).get(self.attribute))
            if value >= self.min and value <= self.max:
                elements.append(element)
        return elements


class TimeFilter(Filter):
    """removes all elements without "attribute" which value is not 
    inside a time window
    """
    def __init__(self, attribute, min =datetime.time.min, max=datetime.time.max, parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.attribute = attribute
        self.mini = min
        self.maxi = max

    def assignRange(self, min, max):
        self.mini = min
        self.maxi = max

    def potentialRange(self):
        """returns a min, max tupel that could be used for filtering"""
        values = []
        for candidate in self.root.output():
            values.append(dateutil.parser.parse(candidate.get(self.attribute)).time())
        return (min(values), max(values))

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = dateutil.parser.parse(element.get(self.attribute)).time()
            if value >= self.mini and value <= self.maxi:
                elements.append(element)
        return elements

class TimeFilterChild(Filter):
    """removes all elements without a "tag" child with "attribute" which value is not 
    inside time range
    """
    def __init__(self, tag, attribute, min=datetime.time.min, max=datetime.time.max, parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.tag = tag
        self.attribute = attribute
        self.min = min
        self.max = max

    def assignRange(self, min, max):
        self.min = min
        self.max = max

    def potentialRange(self):
        """returns a min, max tupel that could be used for filtering"""
        values = []
        for element in self.root.output():
            for candidate in element.iter(self.tag):
                values.append(dateutil.parser.parse(element.find(".//"+self.tag).get(self.attribute)).time())
        return (min(values), max(values))

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = dateutil.parser.parse(element.find(".//"+self.tag).get(self.attribute)).time()
            if value >= self.min and value <= self.max:
                elements.append(element)
        return elements

class DateFilter(Filter):
    """removes all elements without "attribute" which value is not 
    on set date
    """
    def __init__(self, attribute, date =datetime.date.today(), parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.attribute = attribute
        self.date = date

    def assignDate(self, date):
        self.date = date

    def potentialDates(self):
        """returns a date object set that could be used for filtering"""
        values = set()
        for candidate in self.root.output():
            values.add(dateutil.parser.parse(candidate.get(self.attribute)).date())
        return values

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = dateutil.parser.parse(element.get(self.attribute)).date()
            if value == self.date:
                elements.append(element)
        return elements

class DateFilterChild(Filter):
    """removes all elements without a "tag" child with "attribute" which value is not 
    ón set date
    """
    def __init__(self, tag, attribute, date=datetime.date.today, parent = None, data = None):
        super().__init__(parent=parent, data=data)
        self.tag = tag
        self.attribute = attribute
        self.date = date

    def assignDate(self, date):
        self.date = date

    def potentialDates(self):
        """returns a min, max tupel that could be used for filtering"""
        values = set()
        for element in self.root.output():
            for candidate in element.iter(self.tag):
                values.add(dateutil.parser.parse(candidate.get(self.attribute)).date())
        return values

    def output(self):
        self.data = self.parent.output() if self.parent is not None else self.data
        elements =[]
        for element in self.parent.output():
            value = dateutil.parser.parse(element.find(".//"+self.tag).get(self.attribute)).date()
            if value == self.date:
                elements.append(element)
        return elements