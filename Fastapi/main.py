from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,computed_field
from typing import List, Optional,Annotated,Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(...,max_length = 10, title = 'Patient ID', description = 'unique Id')]
    name:Annotated[str, Field(...,max_length =50, title = 'Patient Name', description = "Name of the patient, should be less than 50 characters")]
    age: Annotated[int, Field(...,gt=0, lt=100)]
    city:Annotated[str, Field(...,max_length = 50, title = 'City', description = 'City where patient lives')]
    gender: Annotated[Literal['male','female','other'], Field(..., description = 'Gender of the patient')]
    height:Annotated[float, Field(...,gt=0, description = 'Height of the patient in meters')]
    weight:Annotated[float, Field(...,gt=0, description = 'Weight of the patient in kilograms')]
    

    
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/ (self.height)**2, 2)
        return bmi
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi< 25:
            return 'Normal weight'
        elif self.bmi<30:
            return 'Overweight'
        else:            
            return 'Obese' 
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=100)]
    city: Annotated[Optional[str], Field(default=None, max_length = 50)]
    gender: Annotated[Optional[Literal['male','female','other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
MODEL_VERSION = '1.0.0'
def load_patients():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)
    
@app.get("/")
def hello():
    return {"message": "Patients Management system API"}
@app.get('/')
def home():
    return {'message': 'Welcome to the Patients Management System API'}
@app.get('/health')
def health():
    return {
        'message': 'API is running smoothly',
        'version': MODEL_VERSION
    }


@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patients records "}
@app.get("/view")
def view():
    data = load_patients()
    return data
@app.get("/patients/{patient_id}")
def get(patient_id: str = Path(..., description = 'ID of the patient to retrieve', example= 'P001')):
    data = load_patients()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "patient not found")
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description = 'sort on the basis of height, weight or bmi' ),order: str = Query('asc', description = ' sort in asc or desc order')):
    data = load_patients()
    valid_fielst = ['height','weight','bmi']
    if sort_by not in valid_fielst:
        raise HTTPException(status_code  = 400, detail = 'Invalid request')
    if order not in ['asc','desc']:
        raise HTTPException(status_code = 400, detail = 'Invalid request')
    sort_order = True if order =='desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by,0), reverse = sort_order)
    return sorted_data
@app.post('/create')
def create(patient: Patient):
    # load existing data
    data = load_patients()
    # chedk if patient id already exists
    # it not then add new patient to data and save it back to json file
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = 'Patient with this ID already exists')
    
    patient[patient.id] = patient.model_dump(exclude=[id])
    
    #save the data
    save_data(data)
    return JSONResponse(content = {"message": "Patient created successfully"}, status_code = 201)
@app.put('/edit/{patient_id}')
def edit(patient_id: str, patient_update: PatientUpdate):
    data = load_patients()
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = 'Patient not found')
    existing_patient_data = data[patient_id]
    updated_patient_data = patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_data.items():
        existing_patient_data[key] = value
    existing_patient_data['id'] = patient_id
    updated_patient = Patient(**existing_patient_data)
    existing_patient_data = updated_patient.model_dump(exclude=['id'])
    
    data[patient_id] = existing_patient_data
    save_data(data)
    return JSONResponse(content = {"message": "Patient updated successfully"}, status_code = 200)
@app.delete('/delete/{patient_id}')
def delete(patient_id: str):
    # load the data
    data = load_patients()
    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = 'Patient not found')
    # delete the patient record from data and save it back to json file
    del data[patient_id]
    save_data(data)
    return JSONResponse(content = {"message": "Patient deleted successfully"}, status_code = 200)
