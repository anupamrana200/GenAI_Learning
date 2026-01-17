from fastapi import FastAPI, Path, HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from database import fetch_all_patients, fetch_patient_by_id, insert_patient, update_patient_by_id, delete_patient_by_id


app = FastAPI()

class Patient(BaseModel):
  id: Annotated[str, Field(..., description= "ID of the patient", examples=["P001", "P002"])]
  name: Annotated[str, Field(..., description="Name of the patient, Write the full name.")]
  city: Annotated[str, Field(..., description="City, in which patient lives.")]
  age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient in yrs.")]
  gender: Annotated[Literal['male','female','others'], Field(..., description="Gender of the patient.")]
  height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters.")]
  weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in KGs.")]

class PatientUpdate(BaseModel):
  name: Annotated[Optional[str], Field(default= None ,description="Name of the patient, Write the full name.")]
  city: Annotated[Optional[str], Field(default= None ,description="City, in which patient lives.")]
  age: Annotated[Optional[int], Field(default= None ,gt=0, lt=120, description="Age of the patient in yrs.")]
  gender: Annotated[Optional[Literal['male','female','others']], Field(default= None ,description="Gender of the patient.")]
  height: Annotated[Optional[float], Field(default= None ,gt=0, description="Height of the patient in meters.")]
  weight: Annotated[Optional[float], Field(default= None ,gt=0, description="Weight of the patient in KGs.")]


@app.get("/")
def hello():
  return {"message": "Patient management system api."}

@app.get("/about")
def about():
  return {"message": "TThis is a simple patient management system API built with FastAPI."}  


@app.get("/view")
def view():
    return fetch_all_patients()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples=["P001", "P002"])):
    patient = fetch_patient_by_id(patient_id)

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


@app.post("/create")
def create_patient(patient: Patient):
    try:
        insert_patient(patient.model_dump())
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists or invalid data"
        )

    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully"}
    )


@app.put("/edit/{patient_id}")
def update_patient( patient_update: PatientUpdate, patient_id: str = Path(..., description="ID of the patient to update")):
    existing_patient = fetch_patient_by_id(patient_id)

    if existing_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    updated_data = patient_update.model_dump(exclude_unset=True)

    if not updated_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_patient_by_id(patient_id, updated_data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient updated successfully"}
    )

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    existing_patient = fetch_patient_by_id(patient_id)

    if existing_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    delete_patient_by_id(patient_id)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient deleted successfully"}
    )

