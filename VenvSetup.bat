@echo off

python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
pip install -r app\requirements.txt