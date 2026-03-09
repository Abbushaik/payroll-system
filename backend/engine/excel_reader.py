import pandas as pd
import json


def read_excel_to_json(file_path):
    """
    Reads employee Excel file and converts to JSON format.
    """
    # ── Read Excel file ───────────────────────────────────────────────
    df = pd.read_excel(file_path)

    # ── Rename columns to standard format ────────────────────────────
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # ── Required columns check ────────────────────────────────────────
    required_columns = [
        "employee_id", "employee_name", "department",
        "designation", "level", "date_of_joining", "basic_salary"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # ── Convert to JSON format ────────────────────────────────────────
    employees = []
    for _, row in df.iterrows():
        employee = {
            "employee_id"   : str(row["employee_id"]),
            "name"          : str(row["employee_name"]),
            "department"    : str(row["department"]),
            "designation"   : str(row["designation"]),
            "level"         : str(row["level"]),
            "joining_date"  : str(row["date_of_joining"]).split(" ")[0],
            "basic_salary"  : float(row["basic_salary"])
        }
        employees.append(employee)

    return {"employees": employees}