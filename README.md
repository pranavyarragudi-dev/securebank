# SecureBank - Professional Banking Application

A comprehensive Flask-based banking application with role-based access control, secure authentication, and multi-region architecture support.

## Features

### Customer Features
- **Account Management**: Create and manage checking and savings accounts
- **Money Transfers**: Secure transfer between accounts with validation
- **Deposits & Withdrawals**: Easy money management with transaction history
- **Transaction History**: Detailed view of all banking activities
- **Dashboard**: Comprehensive overview of accounts and recent activity

### Admin Features
- **System Dashboard**: Real-time monitoring of platform statistics
- **User Management**: View and manage all system users
- **Transaction Monitoring**: Oversee all platform transactions
- **System Health**: Monitor component status and performance metrics
- **Security Oversight**: Comprehensive security status monitoring

### Security Features
- **Role-Based Access Control (RBAC)**: Separate customer and admin interfaces
- **Secure Authentication**: Password hashing with Werkzeug
- **CSRF Protection**: Form validation and protection
- **Session Management**: Secure user session handling
- **Input Validation**: Comprehensive form validation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   # If you have the files, navigate to the project directory
   cd securebank
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python setup.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   - Open your browser and go to: `http://localhost:5000`
   - Use the demo credentials provided below

## Demo Credentials

### Customer Account
- **Username**: `customer`
- **Password**: `password`
- **Features**: Account management, transfers, deposits, withdrawals

### Administrator Account
- **Username**: `admin`
- **Password**: `admin123`
- **Features**: System monitoring, user management, transaction oversight

## Project Structure

```
securebank/
├── app.py                          # Application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── setup.py                        # Database initialization script
├── README.md                       # This file
└── banking_app/                    # Main application package
    ├── __init__.py                 # App factory and initialization
    ├── models.py                   # Database models
    ├── forms.py                    # WTForms form definitions
    ├── utils.py                    # Utility functions and decorators
    ├── main/                       # Main blueprint (public pages)
    │   ├── __init__.py
    │   └── routes.py
    ├── auth/                       # Authentication blueprint
    │   ├── __init__.py
    │   └── routes.py
    ├── customer/                   # Customer features blueprint
    │   ├── __init__.py
    │   └── routes.py
    ├── admin/                      # Admin features blueprint
    │   ├── __init__.py
    │   └── routes.py
    └── templates/                  # HTML templates
        ├── base.html               # Base template
        ├── index.html              # Landing page
        ├── auth/                   # Authentication templates
        │   ├── login.html
        │   └── register.html
        ├── customer/               # Customer interface templates
        │   ├── dashboard.html
        │   ├── accounts.html
        │   └── transfer.html
        └── admin/                  # Admin interface templates
            ├── dashboard.html
            └── system_health.html
```

## Key Components

### Database Models
- **User**: Customer and admin user accounts with role-based permissions
- **Account**: Bank accounts (checking/savings) with balance tracking
- **Transaction**: Financial transaction records with full audit trail
- **Role**: User role definitions for access control

### Security Implementation
- **Password Security**: Bcrypt hashing for secure password storage
- **Session Security**: Flask-Login for secure session management
- **Access Control**: Custom decorators for role-based route protection
- **Form Security**: CSRF protection and input validation

### Architecture Highlights
- **Blueprint Organization**: Modular design with separate blueprints for different features
- **Role Separation**: Clear separation between customer and admin functionality
- **Responsive Design**: Mobile-friendly Bootstrap-based interface
- **Security First**: Comprehensive security measures throughout the application

## API Endpoints

### Public Routes
- `GET /` - Landing page
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/register` - Registration page
- `POST /auth/register` - Process registration
- `GET /auth/logout` - User logout

### Customer Routes (Authentication Required)
- `GET /customer/dashboard` - Customer dashboard
- `GET /customer/accounts` - Account management
- `GET /customer/transfer` - Money transfer interface
- `POST /customer/transfer` - Process transfer
- `GET /customer/deposit` - Deposit interface
- `POST /customer/deposit` - Process deposit
- `GET /customer/withdraw` - Withdrawal interface
- `POST /customer/withdraw` - Process withdrawal

### Admin Routes (Admin Role Required)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/accounts` - Account oversight
- `GET /admin/transactions` - Transaction monitoring
- `GET /admin/system_health` - System health monitoring

## Configuration

The application uses environment-based configuration. Key settings in `config.py`:

- **SECRET_KEY**: Flask session encryption key
- **SQLALCHEMY_DATABASE_URI**: Database connection string
- **WTF_CSRF_ENABLED**: CSRF protection toggle
- **TRANSACTION_LIMIT_DAILY**: Daily transaction limit
- **TRANSACTION_LIMIT_SINGLE**: Single transaction limit

## Security Considerations

1. **Change Default Passwords** in production
2. **Set Strong SECRET_KEY** for production deployment
3. **Use HTTPS** for all production traffic
4. **Enable Database Backups** for data protection
5. **Monitor System Logs** for security events
6. **Regular Security Updates** for dependencies

## Production Deployment

For production deployment, consider:

1. **Database Migration**: Move from SQLite to PostgreSQL/MySQL
2. **Environment Variables**: Use environment variables for sensitive configuration
3. **HTTPS Configuration**: Implement SSL/TLS certificates
4. **Load Balancing**: Configure load balancers for high availability
5. **Monitoring**: Implement comprehensive logging and monitoring
6. **Backup Strategy**: Regular database and application backups

## Contributing

This is a demonstration application. For enhancements:

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## License

This project is provided as an educational example. Use responsibly and ensure compliance with financial regulations in your jurisdiction.

## Support

For questions or issues:
1. Check the application logs
2. Verify database connectivity
3. Ensure all dependencies are installed
4. Review the setup instructions

---

**Note**: This is a demonstration application. Do not use for actual financial transactions without proper security auditing and compliance verification.
