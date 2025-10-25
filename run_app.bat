@echo off
echo Starting SecureBank Application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
echo.

REM Setup database
echo Setting up database...
python setup.py
echo.

REM Run application
echo Starting application...
echo Access the application at: http://localhost:5000
echo.
echo Login credentials:
echo   Customer: username=customer, password=password
echo   Admin: username=admin, password=admin123
echo.
python app.py

pause
