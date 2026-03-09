# 💼 PayrollPro — Payroll & Payslip Automation System

A full-stack payroll automation system that reads employee data from Excel, calculates salaries, and generates professional PDF payslips automatically.

---

## 🚀 Features

- 📊 Upload employee data via Excel (.xlsx)
- 💰 Automatic salary calculation per employee level
- 📄 Professional PDF payslip generation
- 📅 Pro-rata salary support for mid-month joiners
- 🎯 Generate payslip for single or all employees
- 🖥️ Modern React UI with drag & drop file upload

---

## 🛠️ Tech Stack

| Layer            | Technology                    |
| ---------------- | ----------------------------- |
| Backend          | Python, FastAPI, Uvicorn      |
| Frontend         | React JS, Tailwind CSS, Axios |
| Excel Processing | Pandas, OpenPyXL              |
| PDF Generation   | ReportLab                     |
| Data Validation  | Pydantic                      |
| Version Control  | Git & GitHub                  |

---

## 📁 Project Structure

```
payroll-system/
├── backend/
│   ├── data/
│   │   └── salary_config.json
│   ├── engine/
│   │   ├── excel_reader.py
│   │   ├── payroll_engine.py
│   │   └── pdf_generator.py
│   ├── models/
│   │   └── schemas.py
│   ├── main.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Header.jsx
    │   │   ├── UploadExcel.jsx
    │   │   ├── EmployeeList.jsx
    │   │   └── PayslipActions.jsx
    │   └── App.jsx
    └── package.json
```

---

## ⚙️ Deduction Rules

| Level   | PF           | Professional Tax | TDS  |
| ------- | ------------ | ---------------- | ---- |
| Intern  | None         | None             | None |
| Junior  | 12% of Basic | ₹200             | None |
| Senior  | 12% of Basic | ₹200             | 5%   |
| Manager | 12% of Basic | ₹200             | 10%  |

---

## 📋 Excel Input Format

Your Excel file must have these columns:

| Column          | Description                        |
| --------------- | ---------------------------------- |
| Employee ID     | Unique ID (e.g. EMP001)            |
| Employee Name   | Full name                          |
| Department      | Department name                    |
| Designation     | Job title                          |
| Level           | Intern / Junior / Senior / Manager |
| Date of Joining | YYYY-MM-DD format                  |
| Basic Salary    | Monthly basic salary amount        |

---

## 🏃 How to Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📄 API Endpoints

| Method | Endpoint               | Description         |
| ------ | ---------------------- | ------------------- |
| GET    | /                      | Health check        |
| POST   | /upload-excel          | Upload Excel file   |
| GET    | /employees             | Get all employees   |
| GET    | /generate-payslip/{id} | Generate single PDF |
| GET    | /generate-all-payslips | Generate all PDFs   |
