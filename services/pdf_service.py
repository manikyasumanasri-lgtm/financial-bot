from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.cell(0, 10, "Personal Finance Advisor Bot", align="C", ln=True)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, "Monthly Financial Summary Report", align="C", ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="C")

def generate_financial_report_pdf(total_income, total_expense, balance, category_expenses, recent_expenses, recent_incomes=None):
    pdf = PDFReport()
    pdf.add_page()
    
    # Financial Overview
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Financial Overview", ln=True)
    pdf.set_font("Helvetica", "", 12)
    
    pdf.cell(50, 10, "Total Income:")
    pdf.cell(0, 10, f"Rs. {total_income:,.2f}", ln=True)
    
    pdf.cell(50, 10, "Total Expenses:")
    pdf.cell(0, 10, f"Rs. {total_expense:,.2f}", ln=True)
    
    pdf.cell(50, 10, "Net Balance:")
    # Highlight balance in red if negative
    if balance < 0:
        pdf.set_text_color(220, 53, 69)
    else:
        pdf.set_text_color(40, 167, 69)
    pdf.cell(0, 10, f"Rs. {balance:,.2f}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    
    # Income Sources Table
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Income Streams", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(45, 10, "Date", border=1)
    pdf.cell(100, 10, "Source", border=1)
    pdf.cell(45, 10, "Amount", border=1, ln=True)
    
    pdf.set_font("Helvetica", "", 12)
    if not recent_incomes:
        pdf.cell(190, 10, "No income recorded.", border=1, align="C", ln=True)
    else:
        for inc in recent_incomes:
            pdf.cell(45, 10, inc.date.strftime('%Y-%m-%d'), border=1)
            source = (inc.source[:45] + '..') if len(inc.source) > 47 else inc.source
            pdf.cell(100, 10, source, border=1)
            pdf.cell(45, 10, f"Rs. {inc.amount:,.2f}", border=1, ln=True)
            
    pdf.ln(10)
    
    # Expense Breakdown by Category
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Expenses by Category", ln=True)
    pdf.set_font("Helvetica", "", 12)
    
    if not category_expenses:
        pdf.cell(0, 10, "No expenses recorded.", ln=True)
    else:
        for cat, amt in category_expenses:
            pdf.cell(60, 10, f"{cat}:")
            pdf.cell(0, 10, f"Rs. {amt:,.2f}", ln=True)
            
    pdf.ln(10)
    
    # Recent Expenses Table
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Recent Transactions", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(35, 10, "Date", border=1)
    pdf.cell(45, 10, "Category", border=1)
    pdf.cell(75, 10, "Description", border=1)
    pdf.cell(35, 10, "Amount", border=1, ln=True)
    
    pdf.set_font("Helvetica", "", 12)
    if not recent_expenses:
        pdf.cell(190, 10, "No recent transactions.", border=1, align="C", ln=True)
    else:
        for exp in recent_expenses:
            pdf.cell(35, 10, exp.date.strftime('%Y-%m-%d'), border=1)
            pdf.cell(45, 10, exp.category, border=1)
            # Truncate description if too long
            desc = (exp.description[:35] + '..') if len(exp.description) > 37 else exp.description
            pdf.cell(75, 10, desc, border=1)
            pdf.cell(35, 10, f"Rs. {exp.amount:,.2f}", border=1, ln=True)
            
    return pdf.output()
