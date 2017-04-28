from .feline import *

class Cat(Feline):
    def __init__(self, kind='Cat', age=0,weight=0, name = 'None',owner='None'):
        Feline.__init__(self, kind, age, weight)
        self.setName(name)
        self.setOwner(owner)

    def setName(self, value):
        self.__name=value
    def setOwner(self, value):
        self.__owner=value

    def getName(self):
        return self.__name    
    def getOwner(self):
        return self.__owner
    
    def getFromForm(self, q):
        Feline.getFromForm(self, q)
        self.setKind('Cat')
        self.setName(q.getfirst('Name', None))
        self.setOwner(q.getfirst('Owner', None))
    
    def getInputs(self, q):
        kind = q.getfirst('Kind', self.getKind())
        age = q.getfirst('Age', self.getAge())
        weight = q.getfirst('Weight', self.getWeight())
        name = q.getfirst('Name', self.getName())
        owner = q.getfirst('Owner', self.getOwner())
        return """ <input value=Cat type="text" name="Kind" style="display: none;">
                   <input placeholder="input age" value={0} type="text" name="Age">
                   <input placeholder="input weight" value={1} type="text" name="Weight">
                   <input placeholder="input name" value={2} type="text" name="Name">
                   <input placeholder="input owner's name" value={3} type="text" name="Owner">""".format(age, weight, name, owner)
        
    def print_object(self):
        return '<td>' + str(self.getKind()) + '</td><td>' + str(self.getAge()) + '</td><td>' + str(self.getWeight()) + '</td><td>' + str(self.getName()) + '</td><td>' + str(self.getOwner()) + '</td>'       
    
