from pydantic import BaseModel

class Address(BaseModel):
  street: str
  city: str
  pincode: str
  state: str
  country: str

class patient(BaseModel):
  name: str
  age: int
  address: Address


address_dict = {'street': '123 Main St', 'city': 'New York', 'pincode': '10001', 'state': 'NY', 'country': 'USA'}
address1 = Address(**address_dict)

patient_info = {'name': 'John Doe', 'age': 30, 'address': address1}
patient1 = patient(**patient_info)

print(patient1)
print(patient1.address.city)