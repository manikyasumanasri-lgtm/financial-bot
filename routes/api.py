from flask import Blueprint, jsonify, session
from database.models import db, Income, Expense
from sqlalchemy import func
from services.ai_service import generate_financial_advice

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/generate_advice', methods=['POST'])
def generate_advice():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = session['user_id']
    
    # Gather data for AI
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.0
    
    category_expenses = db.session.query(
        Expense.category, func.sum(Expense.amount)
    ).filter_by(user_id=user_id).group_by(Expense.category).all()
    
    expenses_dict = {cat: amt for cat, amt in category_expenses}
    
    recent_exps = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).limit(10).all()
    recent_list = [{"category": e.category, "amount": e.amount, "desc": e.description} for e in recent_exps]
    
    advice_markdown = generate_financial_advice(total_income, expenses_dict, recent_list)
    
    return jsonify({'advice': advice_markdown})

@api_bp.route('/export_summary', methods=['POST'])
def export_summary():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = session['user_id']
    
    # Calculate totals for the summary report
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.0
    total_expense = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0.0
    balance = total_income - total_expense
    
    # Mock exports to Google Sheets and Notion
    from services.notion_service import NotionService
    from services.sheets_service import GoogleSheetsService
    from datetime import datetime
    
    notion = NotionService()
    sheets = GoogleSheetsService()
    
    current_month = datetime.now().strftime("%B %Y")
    
    # Send to Notion
    notion_success = notion.export_summary(
        database_id="user_finance_db",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )
    
    # Send to Sheets
    sheet_data = [current_month, total_income, total_expense, balance]
    from utils.config import Config
    sheets_success = sheets.append_row(
        webhook_url=Config.GOOGLE_SHEET_WEBHOOK_URL,
        data_list=sheet_data
    )
    
    if sheets_success:
        return jsonify({
            'success': True,
            'message': 'Monthly summary successfully exported to Google Sheets.',
            'notion_status': notion_success,
            'sheets_status': sheets_success
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to connect to Google Sheets Webhook. Please check the URL in your .env file.',
            'notion_status': notion_success,
            'sheets_status': sheets_success
        }), 500

@api_bp.route('/download_pdf', methods=['GET'])
def download_pdf():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = session['user_id']
    
    # Calculate totals
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.0
    total_expense = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0.0
    balance = total_income - total_expense
    
    category_expenses = db.session.query(
        Expense.category, func.sum(Expense.amount)
    ).filter_by(user_id=user_id).group_by(Expense.category).all()
    
    recent_exps = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).limit(15).all()
    recent_incomes = Income.query.filter_by(user_id=user_id).order_by(Income.date.desc()).limit(15).all()
    
    from services.pdf_service import generate_financial_report_pdf
    pdf_bytes = generate_financial_report_pdf(total_income, total_expense, balance, category_expenses, recent_exps, recent_incomes)
    
    from flask import send_file
    import io
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='Monthly_Financial_Report.pdf'
    )
