from .group import *
import sqlite3
import cgi

connection = sqlite3.connect('cgi-bin/st37/db37.db')
cursor = connection.cursor()
    
def main(q, selfurl):
    flist = Group(q, selfurl)
    
    actions = {
        'add': flist.add,
        'edit': flist.edit,
        'del': flist.fdel,
        'show': flist.fshow,
        'load': flist.fload,
        'remoteload': flist.getRemoteData
    }
    
    styleString = """ *{
    text-align: center;
    color: blue;
    font-family: 'Lobster', cursive;
    font-weight: bold;
    font-style: italic;
    background-image: -webkit-linear-gradient(#AAF0FF, #000088);
    background-size: cover;
    background-attachment: fixed;
}

h1{
    font-size: 450%;
}

h3{
    font-size: 200%; 
}

table {
    max-height: 50%;
    left: 10%;
    margin: auto;
    position: static;
    max-width: 80%;
    overflow-y: auto;
    max-height: 500px;
}

tr {
    border-bottom: 1px solid #FFF;
    margin-bottom: 5px;
}

th, td {
    padding: 2%;
    font-size: 200%;
    text-align: center;
    font-style: italic;
    width: 13.3333%;
}

th{
    color: cyan;
    background: darkblue;
    border-radius: 43%;
    text-decoration: underline;
}

td{
    color: azure;
    border-radius: 100%;
    background: rgba(100,100,250,.1);
}

.tools{
    background-color: rgba(100,100,250,.0);
}

a:hover{
    color: lime;
    font-size: 125%;
}

a:active{
    color: darkorchid;
}

#back{
    float: left;
}

#fileLoad{
    float: right;
}
"""

    headString = """ <!DOCTYPE html>
<html>
    <head>
        <title>The Cat Family</title>
        <style>{}</style>
        <link href="https://fonts.googleapis.com/css?family=Lobster" rel="stylesheet">
    </head>""".format(styleString)
    print ("Content-type: text/html; charset=utf-8\n\n")
    print(headString)
    print("""<body>""")

    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS 'felineTable'('Id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'Kind' TEXT, 'Age' INTEGER, 'Weight' INTEGER, 'Name' TEXT, 'Owner' TEXT)""")
    except:
        print('Error in action: Create Database')
        
    action = q.getfirst('action', None)
        
    if action != 'add' and action != 'edit' and action != 'del':
        if action =='load':
            actions['load'](q, selfurl)
        if action == 'remoteload':
            actions['remoteload'](q, selfurl)
        actions['show'](q, selfurl)
    else:
        actions[action](q, selfurl)    
    print("</body></html>")   
  

if __name__=='__main__':
    main()

