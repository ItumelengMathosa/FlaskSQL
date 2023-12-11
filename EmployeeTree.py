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


    def print_tree(self, indent=0):
        print(self.name)
        if len(self.children) > 0:
            for child in self.children:
                child.print_tree()

    def generate_tree_html(self):
        #creates first list item with self.name as value to be displayed
        #\'{self.name}\' converts self.name to a string object for the HandleNodeClick function
        html = f'<li id="\'{self.ID}\'"><span onclick="HandleNodeClick(\'{self.Name}\',\'{self.ID}\',\'{self.ManagerID}\')">{self.Name}<br>{self.Role}</span>'
        
        if self.children:
            #if self.name has children, create unordered list and call the function recursively for each child
            html += '<ul>'
            for child in self.children:
                html += child.generate_tree_html()
            #add unordered list closing tag
            html += '</ul>'
        #add list item closing tag
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

def DeleteEmployeeFromDataBase(employee):
    db.collection("Employees").document(str(employee.EmployeeNumber)).delete()
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
