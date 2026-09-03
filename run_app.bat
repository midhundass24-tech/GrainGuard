@echo off
title GrainGuard Launch Controller
echo Starting GrainGuard...
py run_app.py
if %ERRORLEVEL% NEQ 0 (
    python run_app.py
)
pause
