@echo off
set PYTHON=python
%PYTHON% -m PyInstaller --clean --onefile --add-data "fptr10.dll;." kkt_info.py
pause