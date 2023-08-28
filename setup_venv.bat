pushd %~dp0
pip install pipenv
md .venv
pipenv install
pause