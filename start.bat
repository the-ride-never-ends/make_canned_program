@echo off
REM Echo to indicate start of the program
echo STARTING PROGRAM...

REM Create a timestamp for the log file name
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set LOGFILE=python_errors_%datetime:~0,8%_%datetime:~8,6%.txt

REM Activate the virtual environment
call venv\Scripts\activate.bat 2>>"%LOGFILE%" || (
    echo Error activating virtual environment. Check log file: %LOGFILE%
    goto :error
)

REM Echo to indicate the start of the Python script
echo *** BEGIN PROGRAM ***

REM Run the Python script
python main.py

REM Echo to indicate the end of the Python script
echo *** END PROGRAM ***

REM Deactivate the virtual environment
call deactivate 2>>"%LOGFILE%" || (
    echo Error deactivating virtual environment. Check log file: %LOGFILE%
    goto :error
)
REM Echo to indicate program completion
echo PROGRAM EXECUTION COMPLETE.
exit /b 0

:error
echo Error occurred. See log file for details: %LOGFILE%
timeout /t 30
exit /b 1