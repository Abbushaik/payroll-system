import json
import calendar
from datetime import datetime


def load_json(filepath):
    """Load JSON data from a file."""
    with open(filepath, "r") as f:
        return json.load(f)


def calculate_prorata(basic_salary, joining_date, month, year):
    """
    Calculate pro-rata salary for mid-month joiners.
    Formula: (Working Days / Total Days in Month) x Basic Salary
    """
    joining = datetime.strptime(joining_date, "%Y-%m-%d")

    # Check if joining month matches current payroll month
    if joining.month == month and joining.year == year:
        total_days  = calendar.monthrange(year, month)[1]
        days_worked = total_days - joining.day + 1
        prorata_salary = round((days_worked / total_days) * basic_salary, 2)
        return prorata_salary, days_worked, total_days

    return basic_salary, None, None


def calculate_payslip(employee, config, month, year):
    """
    Core calculation engine — calculates full payslip for one employee.
    """
    level        = employee["level"]
    basic_salary = employee["basic_salary"]
    joining_date = employee["joining_date"]

    # ── Step 1: Pro-rata check ────────────────────────────────────────
    basic_salary, days_worked, total_days = calculate_prorata(
        basic_salary, joining_date, month, year
    )

    # ── Step 2: Get config for this level ─────────────────────────────
    level_config      = config["salary_config"][level]
    hra_percent       = level_config["allowances"]["hra_percent"]
    travel_allowance  = level_config["allowances"]["travel_allowance"]
    medical_allowance = level_config["allowances"]["medical_allowance"]
    pf_percent        = level_config["deductions"]["pf_percent"]
    professional_tax  = level_config["deductions"]["professional_tax"]
    tds_percent       = level_config["deductions"]["tds_percent"]

    # ── Step 3: Calculate Earnings ────────────────────────────────────
    hra            = round(basic_salary * (hra_percent / 100), 2)
    gross_salary   = round(basic_salary + hra + travel_allowance + medical_allowance, 2)

    # ── Step 4: Calculate Deductions ──────────────────────────────────
    pf               = round(basic_salary * (pf_percent / 100), 2)
    tds              = round(basic_salary * (tds_percent / 100), 2)
    total_deductions = round(pf + tds + professional_tax, 2)

    # ── Step 5: Net Salary ────────────────────────────────────────────
    net_salary = round(gross_salary - total_deductions, 2)

    # ── Step 6: Build Payslip JSON ────────────────────────────────────
    payslip = {
        "employee_id"  : employee["employee_id"],
        "name"         : employee["name"],
        "department"   : employee["department"],
        "designation"  : employee["designation"],
        "level"        : level,
        "month"        : datetime(year, month, 1).strftime("%B %Y"),
        "joining_date" : joining_date,
        "prorata": {
            "applied"    : days_worked is not None,
            "days_worked": days_worked,
            "total_days" : total_days
        },
        "earnings": {
            "basic_salary"     : basic_salary,
            "hra"              : hra,
            "travel_allowance" : travel_allowance,
            "medical_allowance": medical_allowance,
            "gross_salary"     : gross_salary
        },
        "deductions": {
            "provident_fund"  : pf,
            "tds"             : tds,
            "professional_tax": professional_tax,
            "total_deductions": total_deductions
        },
        "net_salary": net_salary
    }

    return payslip