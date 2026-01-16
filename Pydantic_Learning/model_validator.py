from pydantic import BaseModel, EmailStr, field_validator, Field, model_validator

#field validator is works only on one field at a time. if we want to validate multiple fields at a time then we have to use the model_validator decorator.

#Here we check if a patient age is above 60 then there should be a emargency phone number is the contact details. if not then raise a validation error.


class test(BaseModel):
  name: str
  age: int
  email: EmailStr
  address: str = "Not Provided" 
  married: bool 
  allergies: list[str] 
  contact_details: dict[str, str]

  @field_validator('email')
  @classmethod
  def validate_email_domain(cls, value):
    allowed_domains = ['hdfc.com', 'sbi.com']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValueError(f'Email domain {domain} is not allowed. Allowed domains are: {allowed_domains}')
    return value
  
  @field_validator('name')
  @classmethod
  def transform_name(cls, value):
    return value.upper()
  

  @model_validator(mode='after')
  def validate_emergency_contact(self):
    if self.age > 60 and 'emergency' not in self.contact_details:
        raise ValueError('Patients older than 60 must have an emergency contact')
    return self


def insert_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been inserted successfully")

def update_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been updated successfully")


patient_info = {'name': 'John Doe', 
                'age': 65,
                'email': 'john.doe@hdfc.com',
                'address': '123 Main St', 
                'married': True, 
                'allergies': ['dust', 'pollen'], 
                'contact_details': {'phone': '452558452121', 'fax': '452-5451-56', 'emergency': '9876543210'}
                }
patient = test(**patient_info) #unpacking the dictionary to match the model fields

insert_patient_data(patient)
update_patient_data(patient)
