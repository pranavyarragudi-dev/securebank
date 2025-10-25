from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from banking_app.admin import bp
from banking_app.models import User, Account, Transaction, Role
from banking_app import db
from banking_app.utils import admin_required
from sqlalchemy import func

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # System statistics
    total_users = User.query.count()
    total_accounts = Account.query.filter_by(is_active=True).count()
    total_balance = db.session.query(func.sum(Account.balance)).scalar() or 0
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_accounts=total_accounts, 
                         total_balance=total_balance,
                         recent_transactions=recent_transactions)

@bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users)

@bp.route('/user/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    accounts = user.accounts.filter_by(is_active=True).all()
    
    # Get all transactions for this user
    all_transactions = []
    for account in accounts:
        transactions = account.get_transactions()
        all_transactions.extend(transactions)
    
    all_transactions = sorted(all_transactions, key=lambda x: x.created_at, reverse=True)[:20]
    
    return render_template('admin/user_detail.html', user=user, accounts=accounts, transactions=all_transactions)

@bp.route('/accounts')
@login_required
@admin_required
def accounts():
    page = request.args.get('page', 1, type=int)
    accounts = Account.query.filter_by(is_active=True).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/accounts.html', accounts=accounts)

@bp.route('/transactions')
@login_required
@admin_required
def transactions():
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False)
    return render_template('admin/transactions.html', transactions=transactions)

@bp.route('/system_health')
@login_required
@admin_required
def system_health():
    # Simulate system health metrics
    health_data = {
        'database': {'status': 'healthy', 'response_time': '5ms'},
        'api': {'status': 'healthy', 'response_time': '12ms'},
        'authentication': {'status': 'healthy', 'response_time': '3ms'},
        'transactions': {'status': 'healthy', 'response_time': '8ms'},
    }
    
    return render_template('admin/system_health.html', health_data=health_data)

@bp.route('/api/health')
@login_required
@admin_required
def health_api():
    # Health check endpoint for monitoring
    return jsonify({
        'status': 'healthy',
        'timestamp': db.func.now(),
        'version': '1.0.0'
    })
