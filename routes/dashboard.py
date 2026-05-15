from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from database.models import db, User, Income, Expense
from sqlalchemy import func
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        # Check if user actually exists in DB
        user = User.query.get(session['user_id'])
        if not user:
            session.pop('user_id', None)
            session.pop('username', None)
            return redirect(url_for('auth.login'))
            
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    
    # Calculate totals
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0.0
    total_expense = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0.0
    balance = total_income - total_expense
    
    # Get expenses by category for chart
    category_expenses = db.session.query(
        Expense.category, func.sum(Expense.amount)
    ).filter_by(user_id=user_id).group_by(Expense.category).all()
    
    chart_labels = [c[0] for c in category_expenses]
    chart_data = [c[1] for c in category_expenses]

    # Recent transactions
    recent_expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', 
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance,
                           chart_labels=chart_labels,
                           chart_data=chart_data,
                           recent_expenses=recent_expenses)

@dashboard_bp.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    user_id = session['user_id']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_income':
            amount = float(request.form.get('amount'))
            source = request.form.get('source')
            new_income = Income(user_id=user_id, amount=amount, source=source)
            db.session.add(new_income)
            db.session.commit()
            flash('Income added successfully!', 'success')
            
        elif action == 'add_expense':
            amount = float(request.form.get('amount'))
            category = request.form.get('category')
            description = request.form.get('description')
            new_expense = Expense(user_id=user_id, amount=amount, category=category, description=description)
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            
        elif action == 'delete_expense':
            expense_id = request.form.get('expense_id')
            expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
            if expense:
                db.session.delete(expense)
                db.session.commit()
                flash('Expense deleted.', 'success')
                
        elif action == 'delete_income':
            income_id = request.form.get('income_id')
            income = Income.query.filter_by(id=income_id, user_id=user_id).first()
            if income:
                db.session.delete(income)
                db.session.commit()
                flash('Income deleted.', 'success')
                
        return redirect(url_for('dashboard.expenses'))
        
    all_expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
    all_incomes = Income.query.filter_by(user_id=user_id).order_by(Income.date.desc()).all()
    
    return render_template('dashboard/expenses.html', expenses=all_expenses, incomes=all_incomes)

@dashboard_bp.route('/ai-planner')
@login_required
def ai_planner():
    return render_template('dashboard/ai_planner.html')
