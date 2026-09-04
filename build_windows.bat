@echo off
setlocal
py -3 -m pip install --upgrade pyinstaller
py -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name "Vynnify Aim Tweaks" --icon vynnify.ico app.py
pause
