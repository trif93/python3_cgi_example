from .feline import *
from .cat import *
import pickle
import sqlite3
import cgi

class Group:

    def __init__(self, q, selfurl):
        self.q=q
        self.selfurl=selfurl
            
    def add(self, q, selfurl):
        action = q.getfirst('action', None)
        if action is not None and action == 'add':
            ttype = q.getfirst('ttype', None)
            if ttype == '1' or ttype == '0':
                self.add_func(q, selfurl, ttype)
            else:
                print ("""<h3>
                <a href="{0}?student={1}&action=add&ttype=0">Add a feline</a> |
                <a href="{0}?student={1}&action=add&ttype=1">Add a cat</a>
                </h3>""".format(selfurl, q['student'].value))         
        else:
            print("<h3>Invalid type!</h3>")
            print(""" <h3 id="back"><a href="{0}?student={1}"><-Back</a></h3>""".format(selfurl, q['student'].value))

    def add_func(self, q, selfurl, ttype):
        elem = Feline()
        formString = """<form action=""" + '"' + selfurl + '"' + ">" + """
        <input value =""" + '"' + q['student'].value + '"' + """type="text" name="student" style="display: none;">
        <input value = add type="text" name="action" style="display: none;">
        <input value = {0} type="text" name="ttype" style="display: none;">""".format(ttype)
        if ttype == '0':
            formString += """ <input placeholder="input kind" type="text" name="Kind">
                              <input placeholder="input age" type="text" name="Age">
                              <input placeholder="input weight" type="text" name="Weight">
                              <input value="Add the feline" type="submit">"""
        else:
            elem = Cat()
            formString += """ <input value="Cat" type="text" name="Kind" style="display: none;">
                              <input placeholder="input age" type="text" name="Age">
                              <input placeholder="input weight" type="text" name="Weight">
                              <input placeholder="input name" type="text" name="Name">
                              <input placeholder="input owner's name" type="text" name="Owner">
                              <input value="Add the cat" type="submit">"""
        formString += """ </form>"""
        print(formString)
        print(""" <h3 id="back"><a href="{0}?student={1}"><-Back</a></h3>""".format(selfurl, q['student'].value))
        elem.getFromForm(q)
        if elem.getKind() is not None and elem.getAge() is not None:
            self.dbAction('insert', elem)
            print(""" <h3>Completed!</h3>""")

    def edit(self, q, selfurl):
        index = q.getfirst('index', None)
        elem = self.getElement(int(index))
        formString = """<form action=""" + '"' + selfurl + '"' + """>
                <input value =""" + '"' + q['student'].value + '"' + """type="text" name="student" style="display: none;">
                <input value = edit type="text" name="action" style="display: none;">
                <input value = """ + index + """ type="text" name="index" style="display: none;">
                {}
                <input  value='Edit' type="submit">
            </form>""".format(elem.getInputs(q))
        print(formString)
        try:
            elem.getFromForm(q)
            print(""" <h3 id="back"><a href="{0}?student={1}"><-Back</a></h3>""".format(selfurl, q['student'].value))
            if (q.getfirst('Kind', None) is not None) and elem.getAge()!=0:
                self.dbAction('update', elem, int(index))
                print(""" <h3>Completed!</h3>""")
        except (ValueError, IndexError):
            print("""<h3>Invalid index!</h3>""")       
            print(""" <h3 id="back"><a href="{0}?student={1}"><-Back</a></h3>""".format(selfurl, q['student'].value))

    
    def fdel(self, q, selfurl):
        index = q.getfirst('index', None)
        if index is not None:
            try:
                self.dbAction('delete', None, int(index))
                self.fshow(q, selfurl)
            except (ValueError, IndexError):
                print("<h3>Invalid index!</h3>")
                print(""" <h3 id="back"><a href="{0}?student={1}"><-Back</a></h3>""".format(selfurl, q['student'].value))
    
    def fshow(self, q, selfurl):
        connection = sqlite3.connect('cgi-bin/st37/db37.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM felineTable')
        data = cursor.fetchall()
        elem=None
        titleString = """<h1>The Cat Family</h1>
        <h3>
        <a id="back" href="{0}"><-Back</a>
        <a href="{0}?student={1}&action=add">Add new feline or cat</a>
        <a id="fileLoad" href="{0}?student={1}&action=load">Load from file</a>
        </h3>""".format(selfurl, q['student'].value)
        
        print(titleString)
        
        tableString = """ <table>
                        <tr>
                            <th>Kind</th>
                            <th>Age</th>
                            <th>Weight</th>
                            <th>Name</th>
                            <th>Owner</th>
                        </tr> """
        for row in data:
            if row[1] != 'Cat':
                elem = Feline(row[1], row[2], row[3])
            else:
                elem = Cat(row[1], row[2], row[3], row[4], row[5])
            tableString += """<tr>""" + elem.print_object() + """
                <td class="tools"><a href={0}?student={1}&action=edit&index={2}>Edit</a></td>
                <td class="tools"><a href={0}?student={1}&action=del&index={2}>Delete</a></td>
                </tr>""".format(selfurl, q['student'].value, row[0])
        print(tableString) 
        connection.commit()
        cursor.close()
        connection.close()
        

    def dbAction(self, action, elem=None, index=-1):
        connection = sqlite3.connect('cgi-bin/st37/db37.db')
        cursor = connection.cursor()
        if not(elem is None):
            kind = elem.getKind()
            age = elem.getAge()
            weight = elem.getWeight()
            if kind == 'Cat':
                name = str(elem.getName())
                owner = str(elem.getOwner())
            else:
                name = '-'
                owner = '-'
            
        if action =='insert':
            cursor.execute("INSERT INTO felineTable ('Kind', 'Age', 'Weight', 'Name', 'Owner') VALUES (?, ?, ?, ?, ?)",(kind, age, weight, name, owner,))
        elif action == 'update':
            cursor.execute("UPDATE felineTable SET Kind=?, Age=?, Weight=?, Name=?, Owner=? WHERE Id=?",(kind, age, weight, name, owner, index,))
        else:
            cursor.execute("DELETE FROM felineTable WHERE Id=?",(index,))
        connection.commit()
        cursor.close()
        connection.close()

        
    def fload(self, q, selfurl):
        connection = sqlite3.connect('cgi-bin/st37/db37.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM felineTable')
        connection.commit()
        cursor.close()
        connection.close()
        with open("cgi-bin/st37/data.dat","rb") as file:
            container = []
            container = pickle.load(file)
        for elem in container:
            self.dbAction('insert', elem)
            

    def getElement(self, index):
        connection = sqlite3.connect('cgi-bin/st37/db37.db')
        cursor = connection.cursor()
        cursor.execute("SELECT Kind, Age, Weight, Name, Owner FROM felineTable WHERE Id=?",(index,))
        data = cursor.fetchone()
        elem = None
        if data[0] == 'Cat':
            elem = Cat(data[0], data[1], data[2], data[3], data[4])
        else:
            elem = Feline(data[0], data[1], data[2])
        connection.commit()
        cursor.close()
        connection.close()
        return elem

    def getRemoteData(self, q, selfurl):
        conn = sqlite3.connect('cgi-bin/st37/db37.db')
        c = conn.cursor()
        c.execute('DELETE FROM felineTable')
        conn.commit()
        c.close()
        conn.close()
        data = q.getfirst("data", None)
        result = re.findall(r'\[\{(.*?)\}\]', data)
        elem=None
        for e in result:
            if (re.search(r'kind: Cat', e) is None):
                if (re.search(r'kind: (.*) age:', e) is not None):
                    name = re.findall(r'kind: (.*) age:', e)[0]
                else :
                    name = " "
                if (re.search(r'age: (.*) weight:', e) is not None):
                    age = re.findall(r'age: (.*) weight:', e)[0]
                else :
                    age = " "
                if (re.search(r'weight: (.*)', e) is not None):
                    weight = re.findall(r'weight: (.*)', e)[0]
                else :
                    weight = " "
                elem = Feline(kind, age, weight)
            else:
                kind = 'Cat'
                if (re.search(r'age: (.*) weight:', e) is not None):
                    age = re.findall(r'age: (.*) weight:', e)[0]
                else :
                    age = " "
                if (re.search(r'weight: (.*) name:', e) is not None):
                    weight = re.findall(r'weight: (.*) name:', e)[0]
                else :
                    weight = " "
                if (re.search(r'name: (.*) owner:', e) is not None):
                    name = re.findall(r'name: (.*) owner:', e)[0]
                else :
                    name = "-"
                if (re.search(r'owner: (.*)', e) is not None):
                    owner = re.findall(r'owner: (.*)', e)[0]
                else :
                    owner = "-"
                elem = Cat(kind, age, weight, name, owner)
            self.dbAction('insert', elem)
        return
