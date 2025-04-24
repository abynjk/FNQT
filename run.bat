@echo off
echo Launching FNQT Dashboard using Anaconda...

:: Activate base conda environment
call "%USERPROFILE%\anaconda3\Scripts\activate.bat"

:: Change to the app directory
cd "C:\Users\abynj\Python Notes\March25\FNQT\nav_dashboard"

:: Run the dashboard
streamlit run app.py

pause
