from fpdf import FPDF

def txt_to_pdf(txt_path, pdf_path):
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Available width = page width - left margin - right margin
    effective_width = pdf.w - pdf.l_margin - pdf.r_margin

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for raw_line in lines:
        line = raw_line.strip()

        # x position ko har baar explicitly reset karo (yeh hi fix hai)
        pdf.set_x(pdf.l_margin)

        if line == "":
            pdf.ln(4)
            continue

        # Agar line ek heading jaisi hai (number se start hoti hai), bold karo
        if line[0].isdigit() and ". " in line[:4]:
            pdf.set_font("Arial", "B", 12)
        else:
            pdf.set_font("Arial", "", 12)

        pdf.multi_cell(effective_width, 8, line)

    pdf.output(pdf_path)
    print(f"PDF created: {pdf_path}")

if __name__ == "__main__":
    txt_to_pdf("data/policies/hr_policy.txt", "data/policies/hr_policy.pdf")