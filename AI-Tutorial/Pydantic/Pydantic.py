from pydantic import BaseModel, EmailStr,Field,field_validator,model_validator,computed_field,ValidationError
from typing import Annotated, List,Optional,Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length =50, title = 'Patient Name', description = "Name of the patient, should be less than 50 characters")]
    age:int = Field(gt=0, lt=120)
    email: EmailStr
    Married: Optional[bool] = None
    allergies: List[str] = Field(max_length = 3, description = 'List of allergies, maximum 3')
    height: float = Field(..., gt=0, description = 'Height of the patient, must be greater than 0')
    weight: float = Field(..., gt=0, description = 'Weight of the patient, must be greater than 0')
    contact_details: dict[str,str]
    
    
    #field validator do the data validation on only single data field and 
    #model validator do the data validation on multiple data fields and also on the whole model
    #We use the computed field when we want to compute a value based on other fields in the model and we want to include that computed value in the model's output for eg. bmi
    @field_validator('email')
    @classmethod
    def validate_email(cls,value):
        valid_domain = ['icici.com','iitj.ac.in']
        domain = value.split('@')[-1]
        if domain not in valid_domain:
            raise ValueError("Invalid email domain")
        else:
            return value
    @field_validator('name')
    @classmethod
    def validate_name(cls,value):
        return value.upper()
    @field_validator('age')
    @classmethod
    def validate_age(cls,value):
        if value < 12 or value > 120:
            raise ValueError("Age must be between 12 and 120")
        else:
            return value
        
    @model_validator(mode = 'after')

    def validate_model(cls, model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError("Emergency contact details are required for patients above 60 years old")
        return model
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight / (self.height/100)**2, 2)
        return bmi

patient_info = {'name': 'Yogendra', 'age': '21', 'email': 'yogendra@iitj.ac.in', 'Married': True, 'allergies': ['peanuts'], 'height': 175.0, 'weight': 70.0, 'contact_details': {'emergency': '1234567890', 'home': '0987654321'}}
patient1 = Patient(**patient_info)      

def get_patient_info(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.Married)
    print(patient.allergies)
    print(patient.height)
    print(patient.weight)
    print(patient.bmi)
    print("inserted successfully")
    print(type(patient.age))
    


def update_patient_info(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("updated successfully")


get_patient_info(patient1)
