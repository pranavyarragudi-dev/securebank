from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from banking_app.customer import bp
from banking_app.models import User, Account, Transaction
from banking_app.forms import TransferForm, DepositForm, WithdrawalForm, CreateAccountForm
from banking_app import db
from banking_app.utils import customer_required

@bp.route('/dashboard')
@login_required
@customer_required
def dashboard():
    accounts = current_user.accounts.filter_by(is_active=True).all()
    recent_transactions = []
    
    for account in accounts:
        transactions = account.get_transactions()[:5]  # Get 5 most recent
        recent_transactions.extend(transactions)
    
    # Sort by date and get top 10
    recent_transactions = sorted(recent_transactions, key=lambda x: x.created_at, reverse=True)[:10]
    
    return render_template('customer/dashboard.html', accounts=accounts, transactions=recent_transactions)

@bp.route('/accounts')
@login_required
@customer_required
def accounts():
    user_accounts = current_user.accounts.filter_by(is_active=True).all()
    return render_template('customer/accounts.html', accounts=user_accounts)

@bp.route('/create_account', methods=['GET', 'POST'])
@login_required
@customer_required
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        account = Account(
            account_type=form.account_type.data,
            balance=form.initial_deposit.data or 0.0,
            user_id=current_user.id
        )
        db.session.add(account)
        
        # If there's an initial deposit, create a transaction record
        if form.initial_deposit.data and form.initial_deposit.data > 0:
            transaction = Transaction(
                transaction_type='deposit',
                amount=form.initial_deposit.data,
                description='Initial deposit',
                to_account_id=account.id
            )
            db.session.add(transaction)
        
        db.session.commit()
        flash(f'{form.account_type.data.title()} account created successfully!', 'success')
        return redirect(url_for('customer.accounts'))
    
    return render_template('customer/create_account.html', form=form)

@bp.route('/transfer', methods=['GET', 'POST'])
@login_required
@customer_required
def transfer():
    form = TransferForm()
    user_accounts = current_user.accounts.filter_by(is_active=True).all()
    
    if form.validate_on_submit():
        # Find source account (default to first checking account)
        from_account = current_user.accounts.filter_by(account_type='checking', is_active=True).first()
        if not from_account:
            flash('No checking account found for transfer', 'danger')
            return redirect(url_for('customer.transfer'))
        
        # Find destination account
        to_account = Account.query.filter_by(account_number=form.to_account.data, is_active=True).first()
        if not to_account:
            flash('Destination account not found', 'danger')
            return render_template('customer/transfer.html', form=form, accounts=user_accounts)
        
        # Check if user has sufficient balance
        if from_account.balance < form.amount.data:
            flash('Insufficient funds', 'danger')
            return render_template('customer/transfer.html', form=form, accounts=user_accounts)
        
        # Perform transfer
        from_account.balance -= form.amount.data
        to_account.balance += form.amount.data
        
        # Create transaction record
        transaction = Transaction(
            transaction_type='transfer',
            amount=form.amount.data,
            description=form.description.data or f'Transfer to {to_account.account_number}',
            from_account_id=from_account.id,
            to_account_id=to_account.id
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Successfully transferred ${form.amount.data:.2f} to account {to_account.account_number}', 'success')
        return redirect(url_for('customer.dashboard'))
    
    return render_template('customer/transfer.html', form=form, accounts=user_accounts)

@bp.route('/deposit', methods=['GET', 'POST'])
@login_required
@customer_required
def deposit():
    form = DepositForm()
    user_accounts = current_user.accounts.filter_by(is_active=True).all()
    
    if form.validate_on_submit():
        # Default to first checking account
        account = current_user.accounts.filter_by(account_type='checking', is_active=True).first()
        if not account:
            flash('No checking account found for deposit', 'danger')
            return redirect(url_for('customer.deposit'))
        
        # Perform deposit
        account.balance += form.amount.data
        
        # Create transaction record
        transaction = Transaction(
            transaction_type='deposit',
            amount=form.amount.data,
            description=form.description.data or 'Cash deposit',
            to_account_id=account.id
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Successfully deposited ${form.amount.data:.2f}', 'success')
        return redirect(url_for('customer.dashboard'))
    
    return render_template('customer/deposit.html', form=form, accounts=user_accounts)

@bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
@customer_required
def withdraw():
    form = WithdrawalForm()
    user_accounts = current_user.accounts.filter_by(is_active=True).all()
    
    if form.validate_on_submit():
        # Default to first checking account
        account = current_user.accounts.filter_by(account_type='checking', is_active=True).first()
        if not account:
            flash('No checking account found for withdrawal', 'danger')
            return redirect(url_for('customer.withdraw'))
        
        # Check sufficient balance
        if account.balance < form.amount.data:
            flash('Insufficient funds', 'danger')
            return render_template('customer/withdraw.html', form=form, accounts=user_accounts)
        
        # Perform withdrawal
        account.balance -= form.amount.data
        
        # Create transaction record
        transaction = Transaction(
            transaction_type='withdrawal',
            amount=form.amount.data,
            description=form.description.data or 'Cash withdrawal',
            from_account_id=account.id
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Successfully withdrew ${form.amount.data:.2f}', 'success')
        return redirect(url_for('customer.dashboard'))
    
    return render_template('customer/withdraw.html', form=form, accounts=user_accounts)

@bp.route('/transactions')
@login_required
@customer_required
def transactions():
    page = request.args.get('page', 1, type=int)
    
    # Get all transactions for user's accounts
    user_accounts = current_user.accounts.filter_by(is_active=True).all()
    all_transactions = []
    
    for account in user_accounts:
        transactions = account.get_transactions()
        all_transactions.extend(transactions)
    
    # Sort by date
    all_transactions = sorted(all_transactions, key=lambda x: x.created_at, reverse=True)
    
    # Paginate manually (for simplicity)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    transactions_page = all_transactions[start:end]
    
    return render_template('customer/transactions.html', transactions=transactions_page)
