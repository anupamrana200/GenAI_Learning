from fastapi import FastAPI, Path, HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class Patient(BaseModel):
  id: Annotated[str, Field(..., description= "ID of the patient", examples=["P001", "P002"])]
  name: Annotated[str, Field(..., description="Name of the patient, Write the full name.")]
  city: Annotated[str, Field(..., description="City, in which patient lives.")]
  age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient in yrs.")]
  gender: Annotated[Literal['male','female','others'], Field(..., description="Gender of the patient.")]
  height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters.")]
  weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in KGs.")]


  @computed_field
  @property
  def bmi(self) -> float:
    bmi = round(self.weight / (self.height**2),2)
    return bmi

  @computed_field
  @property
  def verdict(self) -> str:
    if self.bmi < 18.5:
        return "Underweight"
    elif self.bmi < 25:
        return "Normal"
    elif self.bmi < 30:
        return "Overweight"
    else:
        return "Obese"
    

class PatientUpdate(BaseModel):
  name: Annotated[Optional[str], Field(default= None ,description="Name of the patient, Write the full name.")]
  city: Annotated[Optional[str], Field(default= None ,description="City, in which patient lives.")]
  age: Annotated[Optional[int], Field(default= None ,gt=0, lt=120, description="Age of the patient in yrs.")]
  gender: Annotated[Optional[Literal['male','female','others']], Field(default= None ,description="Gender of the patient.")]
  height: Annotated[Optional[float], Field(default= None ,gt=0, description="Height of the patient in meters.")]
  weight: Annotated[Optional[float], Field(default= None ,gt=0, description="Weight of the patient in KGs.")]




def load_data():
  with open("patients.json", "r") as f:
      data = json.load(f)
  return data

#alternate code for the with open, the with open statement automatically closes the file after its suite finishes, even if an exception is raised.
# f = open("patients.json")
# data = json.load(f)
# f.close()

def save_data(data):
  with open("patients.json", "w") as f:
    json.dump(data, f)
  


app = FastAPI()
@app.get("/")
def hello():
  return {"message": "Patient management system api."}

@app.get("/about")
def about():
  return {"message": "TThis is a simple patient management system API built with FastAPI."}  


@app.get("/view")
def view():
  data = load_data()
  return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(description="The ID of the patient to retrieve", examples=["P001", "P002"])):

  data = load_data() # Load data from the JSON file

  if patient_id in data:
    return data[patient_id]
  raise HTTPException(status_code=404, detail = "patient not found")


@app.get("/sort")
def sort_patients(sort_by: str = Query(description="Sort the basis of height, weight, bmi or age"), order: str = Query("asc", description="Sort order: asc or desc")):
  valid_fields = ["height", "weight", "age"]

  if sort_by not in valid_fields:
    raise HTTPException(status_code = 400, detail = f"Invalid sort_by entered. must be on of {valid_fields}")
  if order not in ["asc", "desc"]:
    raise HTTPException(status_code = 400, detail = "Invalid order entered. must be one of ['asc', 'desc']")
  
  data = load_data()
  sort_order = False if order == "asc" else True
  sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse= sort_order)
  return sorted_data
#how we write query -> /sort?sort_by=height&order=asc


@app.post('/create')
def create_patient(patient: Patient):
  #Load existing data
  data = load_data()

  #check if the patient exists or not
  if patient.id in data:
    raise HTTPException(status_code = 400, detail = "Patient already exists, please enter a new details.")

  #If the patient is new then add to the database(Json File)
  data[patient.id] = patient.model_dump(exclude=["id"])
  save_data(data)

  return JSONResponse(status_code = 201, content = {'message':'Patient created successfully.'})

@app.put('/edit/{patient_id}')
def update_patient(patient_update: PatientUpdate, patient_id: str = Path(..., description="ID of the patient to update", examples=["P001", "P002"])):
  data = load_data()
  if patient_id not in data:
    raise HTTPException(status_code = 404, detail = "Patient not found.")
  
  existing_patient_info = data[patient_id]

  updated_patient_info = patient_update.model_dump(exclude_unset=True) #Here we convert the pydantic object into a dictionary and here exclude_unset = True means, which field is updated only those fields are included others are excluded.

  for key, value in updated_patient_info.items():
    existing_patient_info[key] = value
  
  #data[patient_id] = existing_patient_info
  #After this if we wish then we can dump the data, put there is a problem, if the user update the height and weight then the bmi and verdict will change, this should be handled. so... 

  #existing_patient_info -> pydantic object -> updated bmi + verdict
  existing_patient_info['id'] = patient_id
  patient_pydentic_object = Patient(**existing_patient_info)

  #pydantic object -> dictionary
  existing_patient_info = patient_pydentic_object.model_dump(exclude='id')

  #add this dict to data
  data[patient_id] = existing_patient_info
  save_data(data)

  return JSONResponse(status_code = 200, content = {'message':'Patient Updated Successfully.'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
  data = load_data()

  if patient_id not in data:
    raise HTTPException(status_code = 404, detail = "Patient Not found")
  
  del data[patient_id]
  save_data(data)

  return JSONResponse(status_code = 200, content = {'message':'patient deleted successfully.'})

