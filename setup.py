#!/usr/bin/env python3
"""
SecureBank Setup Script - Creates database and demo users
"""

import os
import sys
from banking_app import create_app, db
from banking_app.models import User, Role, Account, Transaction

def setup_database():
    """Initialize database and create default data"""
    print("🏦 Setting up SecureBank Database...")

    app = create_app()

    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("✅ Database tables created")

        # Create roles
        customer_role = Role(name='customer', description='Regular banking customer')
        admin_role = Role(name='admin', description='System administrator')

        db.session.add(customer_role)
        db.session.add(admin_role)
        db.session.commit()
        print("✅ User roles created")

        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@securebank.com',
            first_name='System',
            last_name='Administrator',
            phone='555-0000',
            role_id=admin_role.id
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()  # Commit admin user first
        print("✅ Admin user created: admin/admin123")

        # Create demo customer user
        customer_user = User(
            username='customer',
            email='customer@example.com',
            first_name='John',
            last_name='Doe',
            phone='555-1234',
            role_id=customer_role.id
        )
        customer_user.set_password('password')
        db.session.add(customer_user)
        db.session.commit()  # Commit customer user first
        print("✅ Customer user created: customer/password")

        # Now create demo accounts with proper user_id
        checking_account = Account(
            account_type='checking',
            balance=2500.00,
            user_id=customer_user.id  # Use the committed user's ID
        )
        savings_account = Account(
            account_type='savings', 
            balance=5000.00,
            user_id=customer_user.id  # Use the committed user's ID
        )

        db.session.add(checking_account)
        db.session.add(savings_account)
        db.session.commit()
        print("✅ Demo accounts created")

        # Create sample transactions
        initial_deposit_checking = Transaction(
            transaction_type='deposit',
            amount=2500.00,
            description='Initial checking deposit',
            to_account_id=checking_account.id
        )

        initial_deposit_savings = Transaction(
            transaction_type='deposit',
            amount=5000.00,
            description='Initial savings deposit',
            to_account_id=savings_account.id
        )

        sample_withdrawal = Transaction(
            transaction_type='withdrawal',
            amount=100.00,
            description='ATM withdrawal',
            from_account_id=checking_account.id
        )

        db.session.add(initial_deposit_checking)
        db.session.add(initial_deposit_savings)
        db.session.add(sample_withdrawal)

        # Update checking balance after withdrawal
        checking_account.balance = 2400.00

        db.session.commit()
        print("✅ Sample transactions created")

        print("\n🎉 SecureBank setup completed successfully!")
        print("=" * 50)
        print("👤 Customer Login: username=customer, password=password")
        print("👨‍💼 Admin Login: username=admin, password=admin123")
        print("🌐 Run app with: python app.py")
        print("🔗 Access at: http://localhost:5000")
        print("=" * 50)

if __name__ == '__main__':
    setup_database()
