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
- 📩 Download or Clone Application to your working directory.

`git clone https://github.com/romaklym/pyguidesktop.git`
- 🗑️ Delete .venv Folder & Pipfile.lock File (if they exist).
- 🏃‍♀️ Run setup_venv.bat file (double-click on the file).
- ⬇️ Download Tesseract and place it in Tesseract-OCR folder in the root directory of the project.
        You can find it here: https://github.com/UB-Mannheim/tesseract/wiki (Under: The latest installer can be downloaded here)

- ✔️ You are ready to use PyGUIDesktop
- 📍 Work can be done is test.py
- 🟢 To execute script run: main.py

Structure of the project:
```PyGUIDesktop/
│
├── assets/
│   └── # Images and files we use as templates (for template_matching for example)
├── images/
│   └── # Screenshots and images used in the project
├── logs/
│   └── # Logs that will be generated after main.py run
│
├── pyguidesktop/
│   ├── __init__.py
│   ├── guidedesktop.py
│   ├── pyguidesktop.py
│   ├── logger.py
│   └── tests.py
│
├── Tesseract-OCR/
│   ├── tesseract.exe
│   └── ...
│
├── .gitignore
├── main.py
├── Pipfile
├── Pipfile.lock
├── README.md
└── setup_venv.bat
```
