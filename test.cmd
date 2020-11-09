@echo off
cls
setlocal EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)

<nul > X set /p ".=."

@echo on
cls

@echo off
call :color 25 "  ###### STARTING MIGRATIONS #####  "


SET PARAM=%~1
IF "%PARAM%"=="-m" (
  shift
  @echo on
  python manage.py makemigrations Users
  python manage.py makemigrations Layout
  python manage.py makemigrations Biblio
  python manage.py makemigrations Trivia
  python manage.py migrate
  @echo off
)

call :color 64 "  ###### STARTING TESTS #####  "

SET PARAM=%~1
IF "%PARAM%" == "" (
  @echo on
  python manage.py test
  @echo off
) ELSE IF "%PARAM%"=="-p" (
  @echo on
  python manage.py test --parallel
  @echo off
)

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
