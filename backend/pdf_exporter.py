from fpdf import FPDF

def generate_pdf_report(violations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(0, 10, "Vaylo – Compliance Violations Report", ln=1, align="C")
    pdf.ln(10)

    if not violations:
        pdf.multi_cell(0, 10, "No violations found in this data.")
    else:
        for v in violations:
            rule = v.get("rule", "-")
            field = v.get("field", "-")
            name = v.get("record", {}).get("name", "-")
            error = v.get("error", "N/A")

            pdf.multi_cell(0, 10, f"""Rule   : {rule}
Field  : {field}
Name   : {name}
Error  : {error}
---""")
            pdf.ln(2)

    return pdf.output(dest="S").encode("latin-1", "ignore")
