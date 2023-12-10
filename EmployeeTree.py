from InitializeFirestore import *

class EmployeeNode:
    def __init__(self, ID=None, name=None, birthdate=None, employeeNumber=None, 
                salary=None, role=None, parentID=None):
        self.ID = ID
        self.name = name
        self.birthdate = birthdate
        self.employeeNumber = employeeNumber
        self.salary = salary
        self.role = role
        self.children = []
        self.parentID = parentID

    def add_child(self, child):
        
        #append child to EmployeeNode instance 'self.children' list
        self.children.append(child)
        #assign EmployeeNode instance as parentID of current child
        child.parentID = self.ID

    def remove_child(self, child):
        #Remove current child node from parentID's 'children' list
        self.children.pop(child)
        #Set child 'parentID'variable to None
        child.parentID=None


    def print_tree(self, indent=0):
        print(self.name)
        if len(self.children) > 0:
            for child in self.children:
                child.print_tree()

    def generate_tree_html(self):
        #creates first list item with self.name as value to be displayed
        #\'{self.name}\' converts self.name to a string object for the HandleNodeClick function
        html = f'<li><span onclick="HandleNodeClick(\'{self.name}\')">{self.name}</span>'
        
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

def BuildTree():
    root = EmployeeNode(0,"Company Name")
    return root

def AddAllEmployeesAsNodesToTree(root, employees):
    NODES = []

    #Create an 'EmployeeTree' node for every 'emp' dictionary in the 'employee' list
    for emp in employees:
        #Checks if a particular employee is not also classified as their own manager
        if emp['ID'] != emp['ManagerID']:

            #Create instance of the 'EmployeeNode' class using dictionary values as class variables
            node = EmployeeNode(emp['ID'],emp['Name'],
            emp['BirthDate'],emp['EmployeeNumber'],
            emp['Salary'],emp['Role'],emp['ManagerID'])

            NODES.append(node)

            #If current EmployeeNode parentID is '0' then add it as a child to 'root'.
            
            if node.parentID == None:
                root.add_child(node)

        else:
            print("Employee can not be their own manager")

    
    hierarchicalList = AssignHierarchy(NODES)

    return hierarchicalList

def AssignHierarchy(NODES):

    for potentialmanager in NODES:

        for potentialsubordinate in NODES:
            #If the subordinate's parentID matches the manager's ID then call EmployeeNode's add_child function
            if potentialsubordinate.parentID == potentialmanager.ID:
                potentialmanager.add_child(potentialsubordinate)

    return NODES

def AddNewEmployee(employee,manager):
    #Call EmployeeNode class function 'add_child'
    manager.add_child(employee)
    return 0

#GetDataFromFirestore()

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
