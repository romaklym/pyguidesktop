# PyGUIDesktop 💻🤖


### 🚧 Framework is under construction 🚧

Desktop Automation Application build with Python 🐍

Built using next libraries:
- 🦾 PyAutoGUI
- 📜 PyTesseract
- 👀 OpenCV
- 🎱 DesktopMagic
- 🔢 Numpy

Available platforms:
- 🟦 Windows

Requirements:
- 🐍 Python 3.9
- 🖥️ Windows Machine

Current setup:
- 📩 Download or Clone Application to your working directory
- 🗑️ Delete .venv Folder & Pipfile.lock File
- 🏃‍♀️ Run setup_venv.bat file
- ⬇️ Download Tesseract and place it in Tesseract-OCR folder in the root directory of the project. 
        You can find it here: https://github.com/UB-Mannheim/tesseract/wiki (Under: The latest installer can be downloaded here)

- 🔄 Change path to access Tesseract at pyguidesktop.py for:
        pyt.pytesseract.tesseract_cmd = "C:/Users/[YOUR USER]/pyguidesktop/Tesseract-OCR/tesseract.exe"
- ✔️ You are ready to use PyGUIDesktop
- 📍 Work can be done is test.py
- 🟢 To execute script run main.py 
