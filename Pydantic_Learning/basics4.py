from pydantic import BaseModel, Field
from typing import Annotated, Optional

#Using the Annotated we can add metadata to the fields.
#Pydantic is smart enough to read the int or float form a string during validation.
#Means if you provide age as '30' it will convert it to int 30.
#To avoid this we can use strict types like - Field(..., strict=True)


class test(BaseModel):
  name: Annotated[str, Field(default="Unknown",min_length=3, max_length=50, title = "Name of the patient", description="Name should be between 3 to 50 characters", examples = ["John Doe", "Jane Smith"])]
  age: int = Field(gt = 18 , lt = 40) 
  address: str = "Not Provided" 
  married: bool 
  allergies: Optional[list[str]] = None; Field(max_length=5) 
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
