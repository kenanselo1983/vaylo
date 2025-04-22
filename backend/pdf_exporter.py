from fpdf import FPDF

def generate_pdf_report(violations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Vaylo - Compliance Violations Report", ln=1, align="C")
    pdf.ln(10)

    for v in violations:
        rule = str(v.get("rule", "")).encode("ascii", "ignore").decode()
        field = str(v.get("field", "")).encode("ascii", "ignore").decode()
        name = str(v.get("record", {}).get("name", "")).encode("ascii", "ignore").decode()
        error = str(v.get("error", "N/A")).encode("ascii", "ignore").decode()

        pdf.multi_cell(0, 10,
            txt=f"Rule: {rule}\nField: {field}\nName: {name}\nError: {error}\n",
        )
        pdf.ln(2)

    return pdf.output(dest="S")
