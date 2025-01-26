import json
import os
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from mangum import Mangum

class Employee(BaseModel):
    name: str
    position: str
    salary: float
    employee_id: Optional[str] = uuid4().hex

EMPLOYEES_FILE = "employees.json"
EMPLOYEES = []

if os.path.exists(EMPLOYEES_FILE):
    with open(EMPLOYEES_FILE, "r") as f:
        EMPLOYEES = json.load(f)

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Management API!"}

@app.get("/list-employees")
async def list_employees():
    return {"employees": EMPLOYEES}

@app.get("/employee/{employee_id}")
async def get_employee(employee_id: str):
    for employee in EMPLOYEES:
        if employee["employee_id"] == employee_id:
            return employee
    raise HTTPException(404, f"Employee ID {employee_id} not found.")

@app.post("/add-employee")
async def add_employee(employee: Employee):
    employee.employee_id = uuid4().hex
    json_employee = jsonable_encoder(employee)
    EMPLOYEES.append(json_employee)
    with open(EMPLOYEES_FILE, "w") as f:
        json.dump(EMPLOYEES, f)
    return {"employee_id": employee.employee_id}

@app.put("/update-employee/{employee_id}")
async def update_employee(employee_id: str, employee: Employee):
    for index, emp in enumerate(EMPLOYEES):
        if emp["employee_id"] == employee_id:
            EMPLOYEES[index] = jsonable_encoder(employee)
            EMPLOYEES[index]["employee_id"] = employee_id
            with open(EMPLOYEES_FILE, "w") as f:
                json.dump(EMPLOYEES, f)
            return {"message": f"Employee {employee_id} updated successfully."}
    raise HTTPException(404, f"Employee ID {employee_id} not found.")

@app.delete("/delete-employee/{employee_id}")
async def delete_employee(employee_id: str):
    for index, emp in enumerate(EMPLOYEES):
        if emp["employee_id"] == employee_id:
            EMPLOYEES.pop(index)
            with open(EMPLOYEES_FILE, "w") as f:
                json.dump(EMPLOYEES, f)
            return {"message": f"Employee {employee_id} deleted successfully."}
    raise HTTPException(404, f"Employee ID {employee_id} not found.")
