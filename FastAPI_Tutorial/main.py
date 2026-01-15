from fastapi import FastAPI, Path, HTTPException,Query
import json

def load_data():
  with open("patients.json", "r") as f:
      data = json.load(f)
  return data

#alternate code for the with open, the with open statement automatically closes the file after its suite finishes, even if an exception is raised.
# f = open("patients.json")
# data = json.load(f)
# f.close()


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
def view_patient(patient_id: str = Path(description="The ID of the patient to retrieve", example="P001, P002")):

  data = load_data() # Load data from the JSON file

  if patient_id in data:
    return data[patient_id]
  raise HTTPException(status_code=404, detail = "patient not found")


@app.get("/sort")
def sort_patients(sort_by: str = Query(description="Sort the basis of height, weight or bmi"), order: str = Query("asc", description="Sort order: asc or desc")):
  valid_fields = ["height", "weight", "bmi", "age"]

  if sort_by not in valid_fields:
    raise HTTPException(status_code = 400, detail = f"Invalid sort_by entered. must be on of {valid_fields}")
  if order not in ["asc", "desc"]:
    raise HTTPException(status_code = 400, detail = "Invalid order entered. must be one of ['asc', 'desc']")
  
  data = load_data()
  sort_order = False if order == "asc" else True
  sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse= sort_order)
  return sorted_data
#how we write query -> /sort?sort_by=height&order=asc