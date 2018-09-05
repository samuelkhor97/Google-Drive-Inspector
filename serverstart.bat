@echo off
if NOT "%VIRTUAL_ENV%"=="" goto MAIN
start cmd /k "cd %~dp0 & venv\Scripts\activate.bat & cd src & start python realmain.py & exit"
goto END
:MAIN
cd %~dp0\src
start python realmain.py
:END
start http://localhost:7878
exit

