@echo off
echo Mise a jour du depot GitHub...
echo.

git add .
if %errorlevel% neq 0 (
    echo Erreur lors de l'ajout des fichiers
    pause
    exit /b 1
)

echo Entrez un message pour le commit (laissez vide pour le message par defaut):
set /p commit_message="Message: "

if "%commit_message%"=="" (
    set commit_message=Mise a jour du code
)

git commit -m "%commit_message%"
if %errorlevel% neq 0 (
    echo Erreur lors du commit
    pause
    exit /b 1
)

git push origin main
if %errorlevel% neq 0 (
    echo Erreur lors du push
    pause
    exit /b 1
)

echo.
echo Succes ! Les changements ont ete pousses sur GitHub.
echo Attendez quelques minutes pour la mise a jour de GitHub Pages.
echo.
pause
