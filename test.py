from InitializeFirestore import *

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

def GenerateEmployeeNumber(employee_id):
    return f'E{employee_id:03d}'

print(GenerateEmployeeNumber(1000))