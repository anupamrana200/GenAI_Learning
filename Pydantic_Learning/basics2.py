from pydantic import BaseModel


#for type validation there are some inbuild types like EmailStr, AnYUrl, etc.
#for using those we have to first import them from pydantic then use them in class model. like - email: EmailStr

class test(BaseModel):
  name: str
  age: int
  address: str = "Not Provided" #this is the default value, to bypass the error if the field is missing.
  married: bool #for make the field optional -> married: Optional[bool] = None
  allergies: list[str] #for make the field optional ->allergies: Optional[list[str]] = None
  contact_details: dict[str, str]


def insert_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been inserted successfully")

def update_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been updated successfully")


patient_info = {'name': 'John Doe', 
                'age': 30, 
                'address': '123 Main St', 
                'married': True, 
                'allergies': ['dust', 'pollen'], 
                'contact_details': {'phone': '452558452121', 'email': 'hdf@gmail.com'}
                }
patient = test(**patient_info) #unpacking the dictionary to match the model fields

insert_patient_data(patient)
update_patient_data(patient)
