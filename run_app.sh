#!/bin/bash
echo "Starting SecureBank Application..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt
echo

# Setup database
echo "Setting up database..."
python setup.py
echo

# Run application
echo "Starting application..."
echo "Access the application at: http://localhost:5000"
echo
echo "Login credentials:"
echo "  Customer: username=customer, password=password"
echo "  Admin: username=admin, password=admin123"
echo
python app.py
