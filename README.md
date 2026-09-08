# OrangeHRM QA Automation Assignment

This repository contains Selenium automation for the [OrangeHRM public demo](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login), implemented with Python, Pytest, and the Page Object Model (POM).

## Automated workflow

```text
Login → PIM → Add 4 employees → Employee List → Verify each employee → Logout
```

The test creates unique employee names and IDs for every run, searches each
employee by Employee ID, verifies the name displayed in the result table, and
prints `Name Verified` once per employee.

## Project structure

```text
.gitignore                 # Excludes local and generated files from Git
README.md                  # Project documentation
pages/
├── __init__.py            # Makes pages a Python package
├── base_page.py       # Shared explicit waits and browser interactions
├── login_page.py      # Login and logout page object
└── pim_page.py        # PIM employee actions and verification
pytest.ini                 # Pytest configuration and import path
requirements.txt           # Python dependencies
tests/
└── test_automation.py # End-to-end Pytest workflow
```

## Prerequisites

- Python 3.10 or later
- Google Chrome
- Internet access on the first run, so `webdriver-manager` can resolve a
  compatible ChromeDriver

The project runs on macOS, Windows, and Linux. No code changes are required for
these platforms.

## Install dependencies

```zsh
python3 -m venv .venv
```

On Windows, use `python` instead of `python3` if that is how Python is installed:

```powershell
python -m venv .venv
```

Activate the virtual environment for your platform:

| Platform | Shell | Command |
|---|---|---|
| macOS / Linux | zsh or bash | `source .venv/bin/activate` |
| Windows | PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows | Command Prompt | `.venv\Scripts\activate.bat` |

Then install dependencies and run the test from the project root:

```zsh
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -s tests/test_automation.py
```

If PowerShell blocks the activation script, run the following command for the
current PowerShell window, then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Expected successful output includes four `Name Verified` messages followed by:

```text
1 passed
```

## VS Code

Open this folder in VS Code and select the Python interpreter inside `.venv`
using **Python: Select Interpreter**. On macOS/Linux it is `.venv/bin/python`;
on Windows it is `.venv\Scripts\python.exe`. You can then run the test from the
Testing panel or the integrated terminal.

## Credentials

The public demo currently displays `Admin` / `admin123`. The test reads
`ORANGEHRM_USERNAME` and `ORANGEHRM_PASSWORD` environment variables first, so
these can be overridden if the demo credentials change.

> The OrangeHRM demo is a shared environment. Employee data may be reset or
> modified by other users between runs.
