@echo off

:: Check Python installation
python --version || (echo Python is not installed. Exiting... & exit /b)

:: Upgrade pip
python -m pip install --upgrade pip

:: Install required packages from requirements.txt
pip install -r requirements.txt

:: Create necessary folders
mkdir document\static\templates

:: Start Flask server
set FLASK_APP=app.py
flask run --host=localhost --port=5000
