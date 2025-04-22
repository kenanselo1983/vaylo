from fpdf import FPDF

def generate_pdf_report(violations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Vaylo – Compliance Violations Report", ln=1, align="C")
    pdf.ln(10)

    for v in violations:
        pdf.multi_cell(0, 10,
            txt=f"❌ Rule: {v['rule']}\nField: {v['field']}\nName: {v['record'].get('name', 'N/A')}\nError: {v.get('error', 'N/A')}\n",
            border=0
        )
        pdf.ln(2)

    return pdf.output(dest="S").encode("latin-1")
