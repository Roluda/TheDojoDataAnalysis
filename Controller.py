import Data
import Filters
import numpy
import dateutil 

class FilterController:
    def __init__(self):
        self.filterOutlet = Filters.Filter()
        self.data = Data.Data()

    def newData(self, filepath):
        self.data.addData(filepath)
        self.filterOutlet= Filters.Filter(data=self.data.database)

    def newFilterOutlet(self, tag = "database"):
        self.filterOutlet = Filters.TagFilter(tag, data = self.data.database)

    def addFilter(self, filter):
        print(len(self.filterOutlet.output()))
        self.filterOutlet.attach(filter)
        self.filterOutlet = filter
        print(len(self.filterOutlet.output()))

def flatElement(element):
    """returns a dictionary which map 
    element and child element attributes to values"""
    def recursiveAdd(ele, dictionary):
        for key, value in ele.attrib.items():
            dictionary[ele.tag+" "+key]=value
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary)
    attributes={}
    recursiveAdd(element, attributes)
    return attributes

def flatElementNumAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers numbers"""
    def recursiveAdd(ele, dictionary):
        for key, value in ele.attrib.items():
            try:
                float(value)
                dictionary[ele.tag+" "+key]=value
            except:
                pass
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary)
    attributes={}
    recursiveAdd(element, attributes)
    return attributes

def flatElementBoolAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers booleans"""
    def recursiveAdd(ele, dictionary):
        for key, value in ele.attrib.items():
            if value in ["true","false","True","False","TRUE","FALSE"]:
                dictionary[ele.tag+" "+key]=value
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary)
    attributes={}
    recursiveAdd(element, attributes)
    return attributes

def flatElementTimeAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers time formats"""
    def recursiveAdd(ele, dictionary):
        for key, value in ele.attrib.items():
            try:
                dateutil.parse(value, True)
                dictionary[ele.tag+" "+key]=value
            except:
                pass
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary)
    attributes={}
    recursiveAdd(element, attributes)
    return attributes

def flatElementLanguageAttributes(element):
    """returns a dictionary which map 
    element and child element attributes 
    to value, only considers language
    (no bools, floats, int, time formats)
    """
    def recursiveAdd(ele, dictionary):
        for key, value in ele.attrib.items():
            try:
                dateutil.parse(value, False)
                break
            except:
                pass
            try:
                float(value)
                break
            except:
                pass
            if value in ["true","false","True","False","TRUE","FALSE"]:
                break
            dictionary[ele.tag+" "+key]=value
        if len(list(ele)) > 0:
            for child in ele:
                recursiveAdd(child, dictionary)
    attributes={}
    recursiveAdd(element, attributes)
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