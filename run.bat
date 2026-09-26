@echo off
echo ============================================================
echo  Starting E-Tongue Liquid Detection System
echo ============================================================

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo Freeing port 5000 from lingering process (PID: %%a)...
    taskkill /f /pid %%a >nul 2>&1
)

python app.py
pause
