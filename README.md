# OrangeHRM QA Assignment

This repository contains the manual deliverable in `QA_Submission.md` and a
Selenium + pytest Page Object Model implementation in `pages/` and `tests/`.

## Run on macOS

```zsh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -s tests/test_automation.py
```

Open this folder in VS Code, select `.venv/bin/python` with **Python: Select
Interpreter**, then use the Testing panel or run the last command in the
integrated terminal. The public demo credentials default to `Admin` / `admin123`;
override them with `ORANGEHRM_USERNAME` and `ORANGEHRM_PASSWORD` if they change.
