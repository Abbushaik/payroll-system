from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from engine.excel_reader import read_excel_to_json
from engine.payroll_engine import calculate_payslip, load_json
from engine.pdf_generator import generate_payslip_pdf
from datetime import datetime
import shutil
import os

app = FastAPI(title="Payroll Automation System")

# ── CORS ──────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load salary config once ───────────────────────────────────────────
CONFIG_FILE = "data/salary_config.json"
config_data = load_json(CONFIG_FILE)

# ── Store uploaded employees in memory ───────────────────────────────
employees_store = []


# ── Route 1: Health check ─────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Payroll System is Running!"}


# ── Route 2: Upload Excel file ────────────────────────────────────────
@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    global employees_store

    # Save uploaded file temporarily
    temp_path = f"data/temp_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Read Excel and convert to JSON
    data = read_excel_to_json(temp_path)
    employees_store = data["employees"]

    # Clean up temp file
    os.remove(temp_path)

    return {
        "message" : "Excel uploaded successfully",
        "total"   : len(employees_store),
        "employees": employees_store
    }


# ── Route 3: Get all employees ────────────────────────────────────────
@app.get("/employees")
def get_employees():
    if not employees_store:
        raise HTTPException(status_code=404, detail="No employees found. Please upload Excel first.")
    return {"employees": employees_store}


# ── Route 4: Generate payslip PDF for one employee ────────────────────
@app.get("/generate-payslip/{employee_id}")
def generate_payslip(employee_id: str):
    now   = datetime.now()
    month = now.month
    year  = now.year

    employee = next(
        (e for e in employees_store if e["employee_id"] == employee_id),
        None
    )

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    payslip  = calculate_payslip(employee, config_data, month, year)
    filepath = generate_payslip_pdf(payslip)

    return FileResponse(
        path=filepath,
        filename=os.path.basename(filepath),
        media_type="application/pdf"
    )


# ── Route 5: Generate payslips for ALL employees ──────────────────────
@app.get("/generate-all-payslips")
def generate_all_payslips():
    if not employees_store:
        raise HTTPException(status_code=404, detail="No employees found. Please upload Excel first.")

    now   = datetime.now()
    month = now.month
    year  = now.year

    generated = []
    for employee in employees_store:
        payslip  = calculate_payslip(employee, config_data, month, year)
        filepath = generate_payslip_pdf(payslip)
        generated.append({
            "employee_id": employee["employee_id"],
            "name"       : employee["name"],
            "file"       : os.path.basename(filepath)
        })

    return {
        "message"  : "All payslips generated successfully",
        "total"    : len(generated),
        "payslips" : generated
    }