from InitializeFirestore import *
import hashlib

employees = [
    {'ID': 101, 'Name': 'John Doe', 'BirthDate': '1990-05-15', 'EmployeeNumber': 'E001', 'Salary': 60000, 'Role': 'Software Engineer', 'ManagerID': None},
    {'ID': 102, 'Name': 'Jane Smith', 'BirthDate': '1985-08-22', 'EmployeeNumber': 'E002', 'Salary': 75000, 'Role': 'Project Manager', 'ManagerID': 101},
    {'ID': 103, 'Name': 'Mike Johnson', 'BirthDate': '1992-02-10', 'EmployeeNumber': 'E003', 'Salary': 80000, 'Role': 'Data Scientist', 'ManagerID': 101},
    {'ID': 104, 'Name': 'Emily Davis', 'BirthDate': '1988-11-30', 'EmployeeNumber': 'E004', 'Salary': 70000, 'Role': 'Business Analyst', 'ManagerID': 102},
    {'ID': 105, 'Name': 'David Wilson', 'BirthDate': '1995-07-18', 'EmployeeNumber': 'E005', 'Salary': 65000, 'Role': 'Software Engineer', 'ManagerID': 101},
    {'ID': 106, 'Name': 'Sophia Lee', 'BirthDate': '1993-04-25', 'EmployeeNumber': 'E006', 'Salary': 70000, 'Role': 'UX Designer', 'ManagerID': 102},
    {'ID': 107, 'Name': 'Chris Carter', 'BirthDate': '1987-09-12', 'EmployeeNumber': 'E007', 'Salary': 80000, 'Role': 'Product Manager', 'ManagerID': 102},
    {'ID': 108, 'Name': 'Olivia Brown', 'BirthDate': '1991-12-05', 'EmployeeNumber': 'E008', 'Salary': 75000, 'Role': 'Software Engineer', 'ManagerID': 101},
    {'ID': 109, 'Name': 'Daniel White', 'BirthDate': '1986-06-20', 'EmployeeNumber': 'E009', 'Salary': 85000, 'Role': 'Data Engineer', 'ManagerID': 103},
    {'ID': 110, 'Name': 'Ava Miller', 'BirthDate': '1994-03-08', 'EmployeeNumber': 'E010', 'Salary': 70000, 'Role': 'Marketing Specialist', 'ManagerID': 107}
]

ValidUsers = [
    {'Username': 'admin1', 'Password':'03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'},
    {'Username': 'admin2', 'Password':'admin2'},
    {'Username': 'admin3', 'Password':'admin3'},
    {'Username': 'admin4', 'Password':'admin4'},
]

def Populate():

    for emp in employees:
        doc_ref = db.collection("Employees").document(emp['EmployeeNumber'])
        doc_ref.set({'ID': emp['ID'], 'Name': emp['Name'], 'BirthDate': emp['BirthDate'], 'EmployeeNumber': emp['EmployeeNumber'], 'Salary': emp['Salary'], 'Role': emp['Role'], 'ManagerID': emp['ManagerID']})
    
    return 0

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


docs = db.collection("Employees").stream()
NODES=[]
for doc in docs:
    node = EmployeeNode()

#Database Methods
#________________________________________________________________________________________________________________________________________________________________________________________________________

def GenerateEmployeeNumber1(employee_id):
    return f'E{employee_id:03d}'

print(GenerateEmployeeNumber(1000))



def DeleteEmployeeFromDataBase1(employeeNumber):
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


def ValidateUser(username, password, users=ValidUsers):
    
    verdict = None

    hashedpassword = Hash(password)

    for user in users:
        if user['Username'] == username:
            if user['Password'] == hashedpassword:
                verdict = True
                return verdict
            else:
                verdict = "Incorrect password"
                return verdict
        else:
            verdict = "Username not found"

    return verdict

def Hash1(value):
    #Use sha256 hashing library
    hasher = hashlib.sha256()
    hasher.update(value.encode('utf-8'))
    hashedvalue = hasher.hexdigest()

    return hashedvalue

#passw = "scrypt:32768:8:1$0Mwyh4ssZ6qBUt15$90caec5e42057dd7393ecf0eb7fc1f56945a9b20fa880fcb91fd9f7d8c1e47ba99517a5d14cfa5fc95c1b9e7ad93d721a02ecbc002b62a2e77b1612d8142642f"
#pass1 = Hash("admin2")
#print(pass1)



#Populate()


















"""
// Function to populate the dropdown with node names from existing <li> elements
        function populateDropdown() {
            var dropdown = document.getElementById('editNodeManagerIdInput');
            var nodeNames = [];

            // Iterate through all <li> elements on the page
            var listItems = document.querySelectorAll('li span p');

            for (var i = 1; i < listItems.length; i++) {
            var span = listItems[i];
            var nodeName = span.textContent.trim(); // Get the text content of the <span> and trim any whitespace
            nodeNames.push(nodeName);
        }

            // Clear existing options
            dropdown.innerHTML = '';

            // Add a default empty option
            var defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = 'Select a Manager';
            dropdown.appendChild(defaultOption);

            // Add options for each node name
            for (var i = 0; i < nodeNames.length; i++) {
                var option = document.createElement('option');
                option.value = nodeNames[i];
                option.text = nodeNames[i];
                dropdown.appendChild(option);
            }
        }

        // Call the function to populate the dropdown
        populateDropdown();"""