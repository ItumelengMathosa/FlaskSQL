from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
from flask_mysqldb import MySQL
import json

from EmployeeTree import *

app = Flask(__name__)

#SQL

"""
employees = [
    {'ID': 1, 'Name': 'CEO', 'ReportsToID': None},
    {'ID': 2, 'Name': 'Manager1', 'ReportsToID': 1},
    {'ID': 3, 'Name': 'Manager2', 'ReportsToID': 1},
    {'ID': 4, 'Name': 'Employee1', 'ReportsToID': 2},
    {'ID': 5, 'Name': 'Employee2', 'ReportsToID': 2},
    {'ID': 6, 'Name': 'Employee3', 'ReportsToID': 3},
    {'ID': 7, 'Name': 'Employee4', 'ReportsToID': 3},
    ]"""

#Configure SQL Connection
#________________________________________________________________________________________________________________________________________________________________________________________________________

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'collegesystem'

db = MySQL(app)
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_




#Configure Session
#________________________________________________________________________________________________________________________________________________________________________________________________________

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

ValidUsers = [
    {'Username': 'admin1', 'password':'admin1'},
    {'Username': 'admin2', 'password':'admin2'},
    {'Username': 'admin3', 'password':'admin3'},
    {'Username': 'admin4', 'password':'admin4'},
]

def ValidateUser(username, password, users=ValidUsers):

    verdict = None

    for user in users:
        if user['Username'] == username:
            if user['password'] == password:
                verdict = True
                return verdict
            else:
                verdict = "Incorrect password"
                return verdict
        else:
            verdict = "User does not exist"
            
    return verdict

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_




#Appliication Routes
#________________________________________________________________________________________________________________________________________________________________________________________________________

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':

        username = request.form.get("username")
        password = request.form.get("password")

        #Validate username and password against list allowed users
        verdict = ValidateUser(username, password)

        if verdict == True:
            session["name"] = request.form.get("username")
            return redirect('/greet')
        elif verdict == "Incorrect password":
            return render_template('login.html',errormessage=verdict,username=username)
        else:
            return render_template('login.html',errormessage=verdict,username=None)


    return render_template('login.html',errormessage=None,username=None)

@app.route('/logout')
def logout(): 
    session["name"] = None
    return redirect('/login')

@app.route('/EmployeeTree')
def EmployeeTree():

    #Creates single node for Tree Structure i.e. the root node
    root = BuildTree()

    #Retrieves data from firestore, and calls other functions to create tree structure using root node
    GetDataFromFirestore(root)

    #Generates html to be displayed on to web page using 'render_template'
    htmlcontent = root.generate_tree_html()

    return render_template("EmployeeTree.html",htmlcontent=htmlcontent)

@app.route('/AddNewEmployee', methods=['POST', 'GET'])
def AddNewEmployee():

    node = EmployeeNode(id,name,birthdate,employeenumber,salary,role,parentid)
    AddNewEmployeeToDatabase(node)

    return redirect('EmployeeTree.html')

@app.route('/DeleteEmployee', methods=['POST','GET'])
def DeleteEmployee():
    node = EmployeeNode(id,name,birthdate,employeenumber,salary,role,parentid)
    DeleteEmployeeFromDataBase(node)
    return redirect('EmployeeTree.html')

@app.route('/EmployeeTable')
def EmployeeTable():
    return render_template("EmployeeTable.html",employees=employees)


@app.route('/greet', methods=['GET','POST'])
def greet():
    return render_template('greet.html', name=session["name"])


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_


#Main method
if __name__ == "__main__":
    app.run(debug=True)