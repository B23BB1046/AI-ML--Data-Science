from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street:str
    HouseNo: str
    city: str
    state:str
class Patient(BaseModel):
    name: str
    age: int
    email: str
    Married: Optional[bool] = None
    allergies: List[str] = []
    height: float
    weight: float
    contact_details: dict[str,str]
    address: Address
address_dict = {'street': '123 Main St', 'HouseNo': '101', 'city': 'New York', 'state': 'Uttar Pradesh'}
address = Address(**address_dict)

patient_info = {'name': 'Yogendra', 'age': 21, 'email': 'yogendra@iitj.ac.in', 'Married': True, 'allergies': ['peanuts'], 'height': 175.0, 'weight': 70.0, 'contact_details': {'emergency': '1234567890', 'home': '0987654321'}, 'address': address}

patient = Patient(**patient_info)
print(patient)
print(patient.address)
print(patient.address.city)
print(patient.address.state)