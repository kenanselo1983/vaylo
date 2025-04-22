from fpdf import FPDF

def generate_pdf_report(violations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Vaylo – Compliance Violations Report", ln=1, align="C")
    pdf.ln(10)

    if not violations:
        pdf.multi_cell(0, 10, "🎉 No violations found in this data.")
    else:
        for v in violations:
            pdf.multi_cell(0, 10, f"""
Rule     : {v.get("rule", "-")}
Field    : {v.get("field", "-")}
Name     : {v.get("record", {}).get("name", "-")}
Error    : {v.get("error", "N/A")}
---""")
            pdf.ln(2)

    return pdf.output(dest="S")
