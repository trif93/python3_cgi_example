class Feline:
    __kind='None'
    __age=0
    __weight=0
    def __init__(self, kind='None',age=0,weight=0):
        self.setKind(kind)
        self.setAge(age)
        self.setWeight(weight)
        
    def setKind(self, value):
        self.__kind = value
    def setAge(self, value):
        self.__age = value
    def setWeight(self, value):
        self.__weight = value

    def getKind(self):
        return self.__kind
    def getAge(self):
        return self.__age
    def getWeight(self):
        return self.__weight

    def getFromForm(self, q):
        self.setKind(q.getfirst('Kind', None))
        self.setAge(q.getfirst('Age', None))
        self.setWeight(q.getfirst('Weight', None)) 
    
    def getInputs(self, q):
        kind = q.getfirst('Kind', self.getKind())
        age = q.getfirst('Age', self.getAge())
        weight = q.getfirst('Weight', self.getWeight())
        return """ <input placeholder="input kind" value={0} type="text" name="Kind">
                   <input placeholder="input age" value={1} type="text" name="Age">
                   <input placeholder="input weight" value={2} type="text" name="Weight">""".format(kind, age, weight)
        
    def print_object(self):
        return '<td>' + str(self.getKind()) + '</td><td>' + str(self.getAge()) + '</td><td>' + str(self.getWeight()) + '</td><td> - </td><td> - </td>'
    
