@echo off
set /p input="Do you want to recommit (Y/n)? "

if /i "%input%"=="y" (
    git reset --soft HEAD~1
    git add .
    git commit
    git push -f
)

cmd /k