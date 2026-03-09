from pydantic import BaseModel
from typing import Optional


class Employee(BaseModel):
    employee_id : str
    name        : str
    department  : str
    designation : str
    level       : str
    joining_date: str
    basic_salary: float


class EmployeeList(BaseModel):
    employees: list[Employee]


class ProrataInfo(BaseModel):
    applied    : bool
    days_worked: Optional[int]
    total_days : Optional[int]


class Earnings(BaseModel):
    basic_salary     : float
    hra              : float
    travel_allowance : float
    medical_allowance: float
    gross_salary     : float


class Deductions(BaseModel):
    provident_fund  : float
    tds             : float
    professional_tax: float
    total_deductions: float


class Payslip(BaseModel):
    employee_id : str
    name        : str
    department  : str
    designation : str
    level       : str
    month       : str
    joining_date: str
    prorata     : ProrataInfo
    earnings    : Earnings
    deductions  : Deductions
    net_salary  : float