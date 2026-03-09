from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os


def generate_payslip_pdf(payslip, output_dir="generated_payslips"):
    """
    Generates a professional PDF payslip for one employee.
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── File name ─────────────────────────────────────────────────────
    month_str = payslip["month"].replace(" ", "_")
    filename  = f"{payslip['employee_id']}_{month_str}_Payslip.pdf"
    filepath  = os.path.join(output_dir, filename)

    doc    = SimpleDocTemplate(filepath, pagesize=A4,
                               rightMargin=15*mm, leftMargin=15*mm,
                               topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    story  = []

    # ── Custom Styles ─────────────────────────────────────────────────
    title_style = ParagraphStyle("title",
        fontSize=20, fontName="Helvetica-Bold",
        textColor=colors.white, alignment=TA_CENTER)

    header_style = ParagraphStyle("header",
        fontSize=10, fontName="Helvetica",
        textColor=colors.white, alignment=TA_CENTER)

    label_style = ParagraphStyle("label",
        fontSize=10, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#333333"))

    value_style = ParagraphStyle("value",
        fontSize=10, fontName="Helvetica",
        textColor=colors.HexColor("#333333"))

    net_style = ParagraphStyle("net",
        fontSize=13, fontName="Helvetica-Bold",
        textColor=colors.white, alignment=TA_CENTER)

    # ── Company Header ────────────────────────────────────────────────
    header_data = [[
        Paragraph("Fadel Software Solutions Pvt. Ltd.", title_style),
    ],[
        Paragraph("11th Floor, Sanali Spazio building, Inorbit Mall Rd, Software Units Layout, Madhapur, Hyderabad, Telangana 500081 | hr@fadelsoft.com", header_style),
    ],[
        Paragraph(f"PAYSLIP — {payslip['month'].upper()}", title_style),
    ]]

    header_table = Table(header_data, colWidths=[180*mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1a73e8")),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 2), (-1, 2), [colors.HexColor("#1558b0")]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8*mm))

    # ── Employee Details ──────────────────────────────────────────────
    emp = payslip
    emp_data = [
        ["Employee ID",  emp["employee_id"],   "Department",   emp["department"]],
        ["Employee Name",emp["name"],           "Designation",  emp["designation"]],
        ["Level",        emp["level"],          "Joining Date", emp["joining_date"]],
        ["Pay Month",    emp["month"],          "", ""],
    ]

    emp_table = Table(emp_data, colWidths=[40*mm, 60*mm, 40*mm, 40*mm])
    emp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f0f4ff")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#f0f4ff")),
        ("FONTNAME",   (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",   (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]))
    story.append(emp_table)
    story.append(Spacer(1, 6*mm))

    # ── Pro-rata Note ─────────────────────────────────────────────────
    if payslip["prorata"]["applied"]:
        note = Paragraph(
            f"⚠ Pro-rata applied: {payslip['prorata']['days_worked']} days worked out of {payslip['prorata']['total_days']} days",
            ParagraphStyle("note", fontSize=9, textColor=colors.HexColor("#e65100"),
                           fontName="Helvetica-Oblique")
        )
        story.append(note)
        story.append(Spacer(1, 4*mm))

    # ── Earnings & Deductions Table ───────────────────────────────────
    e = payslip["earnings"]
    d = payslip["deductions"]

    table_data = [
        # Header row
        ["EARNINGS", "Amount (Rs.)", "DEDUCTIONS", "Amount (Rs.)"],
        ["Basic Salary",      f"{e['basic_salary']:,.2f}",  "Provident Fund",   f"{d['provident_fund']:,.2f}"],
        ["HRA",               f"{e['hra']:,.2f}",           "TDS",              f"{d['tds']:,.2f}"],
        ["Travel Allowance",  f"{e['travel_allowance']:,.2f}", "Professional Tax", f"{d['professional_tax']:,.2f}"],
        ["Medical Allowance", f"{e['medical_allowance']:,.2f}", "", ""],
        ["Gross Salary",      f"{e['gross_salary']:,.2f}",  "Total Deductions", f"{d['total_deductions']:,.2f}"],
    ]

    sal_table = Table(table_data, colWidths=[55*mm, 35*mm, 55*mm, 35*mm])
    sal_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",  (0, 0), (1, 0), colors.HexColor("#1a73e8")),
        ("BACKGROUND",  (2, 0), (3, 0), colors.HexColor("#e53935")),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        # Total rows
        ("BACKGROUND",  (0, 5), (1, 5), colors.HexColor("#e8f5e9")),
        ("BACKGROUND",  (2, 5), (3, 5), colors.HexColor("#fce4e4")),
        ("FONTNAME",    (0, 5), (-1, 5), "Helvetica-Bold"),
        # General
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ALIGN",       (1, 0), (1, -1), "RIGHT"),
        ("ALIGN",       (3, 0), (3, -1), "RIGHT"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]))
    story.append(sal_table)
    story.append(Spacer(1, 6*mm))

    # ── Net Salary ────────────────────────────────────────────────────
    net_data = [[
        Paragraph(f"NET SALARY (Take Home):  Rs. {payslip['net_salary']:,.2f}", net_style)
    ]]
    net_table = Table(net_data, colWidths=[180*mm])
    net_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#1a73e8")),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(net_table)
    story.append(Spacer(1, 6*mm))

    # ── Footer ────────────────────────────────────────────────────────
    footer = Paragraph(
        "This is a system-generated payslip and does not require a signature.",
        ParagraphStyle("footer", fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    )
    story.append(footer)

    # ── Build PDF ─────────────────────────────────────────────────────
    doc.build(story)
    return filepath