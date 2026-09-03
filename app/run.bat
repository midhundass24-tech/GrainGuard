@echo off
title GrainGuard Live Camera App
echo Launching GrainGuard Live Camera Terminal...
rem Ensure we are in the project root directory
cd /d "%~dp0.."
py app/run.py
if %ERRORLEVEL% NEQ 0 (
    python app/run.py
)
pause

