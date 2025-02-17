@echo off
set PYTHONPATH=.\;%PYTHONPATH%

call .\venv\Scripts\activate.bat
py -B mineme_server/src/main.py
call .\venv\Scripts\deactivate.bat