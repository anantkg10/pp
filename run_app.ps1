$python = "C:\Users\HP\Desktop\coding\python\venv\python.exe"

if (-not (Test-Path $python)) {
    Write-Error "Python 3.12 environment not found at $python"
    exit 1
}

& $python manage.py runserver
