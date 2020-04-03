import Data
import Filters
import numpy
import dateutil 

class FilterController:
    def __init__(self):
        self.root = Filters.Filter()
        self.data = Data.Data()

    def newData(self, filepath):
        self.data.addData(filepath)
        self.root = Filters.Filter(data=self.data.database)

    def newFilterTree(self, tag = "database"):
        self.root = Filters.TagFilter(tag, data = self.data.database)
        self.possibleFilters = possibleFilters(self.root.output())

    def addFilter(self, filter):
        self.root.getLeaf().attach(filter)

    def treeOutput(self):
        return self.root.getLeaf().output()

def possibleFilters(data):
    filters = {}
    print(uniqueLanguageAttributesInData(data))
    for attributes in uniqueLanguageAttributesInData(data):
        tag, _ ,att = attributes.rpartition('/')
        if tag[0] == "0":
            filters["Whitelist "+tag+"/"+att] = Filters.WhitelistFilter(att)
        else:
            filters["Whitelist "+tag+"/"+att] = Filters.WhitelistFilterChild(tag[1:], att)
    for attributes in uniqueBoolAttributesInData(data):
        tag, _, att = attributes.rpartition('/')
        if tag[0] == "0":
            filters["Bool "+tag+"/"+att] = Filters.BoolFilter(att)
        else:
            filters["Bool "+tag+"/"+att] = Filters.BoolFilterChild(tag[1:], att)
    for attributes in uniqueNumAttributesInData(data):
        tag, _, att = attributes.rpartition('/')
        if tag[0] == "0":
            filters["Range "+tag+"/"+att] = Filters.RangeFilter(att)
        else:
            filters["Range "+tag+"/"+att] = Filters.RangeFilterChild(tag[1:], att)
    return filters



def flatElement(element):
    """returns a dictionary which map 
    element and child element attributes to values"""
    def recursiveAdd(ele, dictionary, depth):
        for key, value in ele.attrib.items():
            dictionary[str(depth)+ele.tag+"/"+key]=value
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary, depth+1)
    attributes={}
    recursiveAdd(element, attributes, 0)
    return attributes

def flatElementNumAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers numbers"""
    def recursiveAdd(ele, dictionary, depth):
        for key, value in ele.attrib.items():
            try:
                float(value)
                dictionary[str(depth)+ele.tag+"/"+key]=value
            except:
                pass
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary, depth+1)
    attributes={}
    recursiveAdd(element, attributes, 0)
    return attributes

def flatElementBoolAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers booleans"""
    def recursiveAdd(ele, dictionary, depth):
        for key, value in ele.attrib.items():
            if value in ["true","false","True","False","TRUE","FALSE"]:
                dictionary[str(depth)+ele.tag+"/"+key]=value
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary, depth+1)
    attributes={}
    recursiveAdd(element, attributes, 0)
    return attributes

def flatElementTimeAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers time formats"""
    def recursiveAdd(ele, dictionary, depth):
        for key, value in ele.attrib.items():
            try:
                float(value)
                continue
            except:
                pass
            try:
                dateutil.parser.parse(value)
                dictionary[str(depth)+ele.tag+"/"+key]=value
            except:
                pass
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary, depth+1)
    attributes={}
    recursiveAdd(element, attributes, 0)
    return attributes

def flatElementLanguageAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers language
    (no bools, floats, int, time formats)
    """
    def recursiveAdd(ele, dictionary, depth):
        for key, value in ele.attrib.items():
            try:
                float(value)
                continue
            except:
                pass
            try:
                dateutil.parser.parse(value)
                continue
            except:
                pass
            if value in ["true", "false", "True", "False"]:
                continue
            dictionary[str(depth)+ele.tag+"/"+key]=value
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary, depth+1)
    attributes={}
    recursiveAdd(element, attributes, 0)
    return attributes

def uniqueAttributesInData(elements):
    """takes a list of elements and returns a set
    with uique attributes"""
    uniqueAttributes = set()
    for element in elements:
        for key in flatElement(element).keys():
            uniqueAttributes.add(key)
    return uniqueAttributes

def uniqueNumAttributesInData(elements):
    """takes a list of elements and returns a set
    with unique numeric attributes"""
    uniqueAttributes = set()
    for element in elements:
        for key in flatElementNumAttributes(element).keys():
            uniqueAttributes.add(key)
    return uniqueAttributes

def uniqueBoolAttributesInData(elements):
    """takes a list of elements and returns a set
    with unique boolean attributes"""
    uniqueAttributes = set()
    for element in elements:
        for key in flatElementBoolAttributes(element).keys():
            uniqueAttributes.add(key)
    return uniqueAttributes

def uniqueTimeAttributesInData(elements):
    """takes a list of elements and returns a set
    with unique time attributes"""
    uniqueAttributes = set()
    for element in elements:
        for key in flatElementTimeAttributes(element).keys():
            uniqueAttributes.add(key)
    return uniqueAttributes

def uniqueLanguageAttributesInData(elements):
    """takes a list of elements and returns a set
    with unique language attributes, i.e. names"""
    uniqueAttributes = set()
    for element in elements:
        for key in flatElementLanguageAttributes(element).keys():
            uniqueAttributes.add(key)
    return uniqueAttributes