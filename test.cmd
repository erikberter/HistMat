@echo off

setlocal EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)

<nul > X set /p ".=."

@echo on
cls

@echo off
call :color 25 "  ###### STARTING MIGRATIONS #####  "
@echo on

python manage.py migrate

@echo off
call :color 64 "  ###### STARTING TESTS #####  "
@echo on


python manage.py test
@echo off
exit /b

:color

set "param=^%~2" !
set "param=!param:"=\"!"
echo:
findstr /p /A:%1 "." "!param!\..\X" nul
<nul set /p ".=%DEL%%DEL%%DEL%%DEL%%DEL%%DEL%%DEL%"
echo:

exit /b
