from InitializeFirestore import *

class EmployeeNode:
    def __init__(self, ID=None, Name=None, BirthDate=None, EmployeeNumber=None, 
                Salary=None, Role=None, ManagerID=None):
        self.ID = ID
        self.Name = Name
        self.BirthDate = BirthDate
        self.EmployeeNumber = EmployeeNumber
        self.Salary = Salary
        self.Role = Role
        self.children = []
        self.ManagerID = ManagerID

    def add_child(self, child):
        
        #append child to EmployeeNode instance 'self.children' list
        self.children.append(child)
        #assign EmployeeNode instance as ManagerID of current child
        child.ManagerID = self.ID

    def remove_child(self, child):
        #Remove current child node from ManagerID's 'children' list
        self.children.pop(child)
        #Set child 'ManagerID'variable to None
        child.ManagerID=None


    
    def generate_tree_html(self):
        # creates the first list item with self.name and self.Role as values to be displayed
        # HandleNodeClick takes all EmployeeNode class variables as arguments
        # \'{self.name}\' converts self.name to a string object for the HandleNodeClick function
        NodeTitle = f"ID: {self.ID}\n Manager's ID: {self.ManagerID}\n Employee Number: {self.EmployeeNumber}"
        if self.Role is None:
            html = f'<li id="\'{self.ID}\'" title="{NodeTitle}"><span onclick="HandleNodeClick(\'{self.Name}\',\'{self.ID}\',\'{self.ManagerID}\',\'{self.BirthDate}\',\'{self.EmployeeNumber}\',\'{self.Salary}\',\'{self.Role}\')"><p>{self.Name}</p></span>'
        else:
            html = f'<li id="\'{self.ID}\'" title="{NodeTitle}"><span onclick="HandleNodeClick(\'{self.Name}\',\'{self.ID}\',\'{self.ManagerID}\',\'{self.BirthDate}\',\'{self.EmployeeNumber}\',\'{self.Salary}\',\'{self.Role}\')"><p>{self.Name}</p>{self.Role}</span>'

        if self.children:
            # if self.name has children, create an unordered list and call the function recursively for each child
            html += '<ul>'
            for child in self.children:
                html += child.generate_tree_html()
            # add unordered list closing tag
            html += '</ul>'
        # add list item closing tag
        html += '</li>'

        return html





#Tree Structure Methods
#________________________________________________________________________________________________________________________________________________________________________________________________________

def GetDataFromFirestore(root):
    #Create reference employees_ref for 'Employees' collection in Firestore database
    employees_ref = db.collection("Employees").stream()

    
    employees = []

    #Concert every document in collection to dictionary and append to employees list
    for emp in employees_ref:
        employees.append(emp.to_dict())
    
    #function that creates nodes from all dictionaries in employee list,
    #and assigns hierarchy to nodes. 
    AddAllEmployeesAsNodesToTree(root,employees)

    return root

def AddNewEmployeeToDatabase(employee):
    #Creates data variable that is employee node converted to dictionary to be saved to database
    data = employee.__dict__
    #Adds single employee to Firestore database
    db.collection("Employees").document(str(data['EmployeeNumber'])).set(data)
    return 0

def DeleteEmployeeFromDataBase(employeeNumber):
    Doc_to_del = None
    Docs_to_update = []
    Employees = []
    employeeID = None
    managerID = None

    data_ref = db.collection("Employees").stream()
    
    #Make docs from database to dictionary
    for doc in data_ref:
        Employees.append(doc.to_dict())

    

    for emp in Employees:
        if emp['EmployeeNumber'] == employeeNumber:
            Doc_to_del = emp['EmployeeNumber']
            employeeID = emp['ID']
            managerID = emp['ManagerID']

    for emp in Employees:
        if emp['ManagerID'] == employeeID:
            #Appends Docs_to_update with every employee number of the employees whose ManagerID's matches the ID of the
            #employee is getting deleted
            Docs_to_update.append(emp['EmployeeNumber'])


    for EmployeeNumber in Docs_to_update:
        doc_ref = db.collection("Employees").document(str(EmployeeNumber))
        #Updates the current 'EmployeeNumber''s ManagerID to the managerID of the employee that gettin deleted
        doc_ref.update({"ManagerID": managerID})
    
    db.collection("Employees").document(str(Doc_to_del)).delete()

    return 0

def BuildTree():
    root = EmployeeNode(0,"Epi-Use")
    return root

def AddAllEmployeesAsNodesToTree(root, employees):
    NODES = []

    #Create an 'EmployeeTree' node for every 'emp' dictionary in the 'employee' list
    for emp in employees:

        #Create instance of the 'EmployeeNode' class using dictionary values as class variables
        node = EmployeeNode(emp['ID'],emp['Name'],
        emp['BirthDate'],emp['EmployeeNumber'],
        emp['Salary'],emp['Role'],emp['ManagerID'])

        NODES.append(node)

        #If current EmployeeNode ManagerID is '0' then add it as a child to 'root'.
        
        if node.ManagerID == None:
            root.add_child(node)

    
    hierarchicalList = AssignHierarchy(NODES)

    return hierarchicalList

def AssignHierarchy(NODES):

    for potentialmanager in NODES:

        for potentialsubordinate in NODES:
            #If the subordinate's ManagerID matches the manager's ID then call EmployeeNode's add_child function
            if potentialsubordinate.ManagerID == potentialmanager.ID:
                potentialmanager.add_child(potentialsubordinate)

    return NODES

#GetDataFromFirestore()

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
