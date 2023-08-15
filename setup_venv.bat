:: Creates python virtual enviroment in current directory
:: and installs packages specified in Pipfile
:: You need to have Python 3.7 64-bit installed
:: Also if you're running it from domain, you need to have OpenVP running 
:: in order to connect to pypi.org and download packages

pushd %~dp0
pip install pipenv
md .venv
pipenv install
pause