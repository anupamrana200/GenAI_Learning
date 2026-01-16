from pydantic import BaseModel, EmailStr, field_validator, Field

#here we can use the field validator decorator to create custom validation for the fields. like - if the hospital has any tie-up with any banks like hdfc, sbi, then the banks want to treat theieir customers with some special discount. then they will check their patient by the email domain, like hdfc.com, sbi.com, etc. But till now using the EmailStr we can only validate the email format. but we can create a custom validator to check the email domain as well.

#field validator works on two ways, before and after type curation. By default it works after type curation. but if we want to work before type curation then we have to pass the pre=True parameter in the decorator. or @field_validator('name', mode = 'before')

#field validator is works only on one field at a time. if we want to validate multiple fields at a time then we have to use the model_validator decorator.


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



def insert_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been inserted successfully")

def update_patient_data(patient: test):
  print(f"The patient {patient.name} whom age is {patient.age} and address is {patient.address} has been updated successfully")


patient_info = {'name': 'John Doe', 
                'age': 30,
                'email': 'john.doe@hdfc.com',
                'address': '123 Main St', 
                'married': True, 
                'allergies': ['dust', 'pollen'], 
                'contact_details': {'phone': '452558452121', 'fax': '452-5451-56'}
                }
patient = test(**patient_info) #unpacking the dictionary to match the model fields

insert_patient_data(patient)
update_patient_data(patient)
