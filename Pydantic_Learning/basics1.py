from pydantic import BaseModel

class test(BaseModel):
  name: str
  age: int
  address: str

def insert_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been inserted successfully")

def update_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been updated successfully")


patient_info = {'name': 'John Doe', 'age': 30, 'address': '123 Main St'}
patient = test(**patient_info) #unpacking the dictionary to match the model fields

insert_patient_data(patient)
update_patient_data(patient)
