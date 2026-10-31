# Nam's system tests (T002–T004) – "Your Store" OpenCart demo

Automated system tests for 31282/32571 Assignment 3, written in Python with pytest and Selenium WebDriver (Google Chrome).

Site under test: https://opencart.abstracta.us/

| File | Test case | Function |
| --- | --- | --- |
| `tests/test_tc02_registration.py` | T002 | F2 User Registration |
| `tests/test_tc03_compare.py` | T003 | F3 Comparing Products |
| `tests/test_tc04_add_to_cart.py` | T004 | F4 Adding a Product to Shopping Cart |
| `helpers.py` | shared | page locators, waits, screenshots, one action per function |
| `conftest.py` | shared | opens/closes Chrome for each test, registers the account T002 reuses, screenshots failures |
| `check_env.py` | setup | prints OS, CPU, Python/Selenium/pytest/Chrome versions |

Each test file has one function per scenario (S1 success, S2 invalid inputs, S3 boundary/edge inputs);
every input inside a scenario runs as its own check and has its own screenshot.

## Set up (Windows, PowerShell, inside this folder)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python check_env.py
```

## Run

```powershell
pytest tests/test_tc02_registration.py                          # one test case
pytest --html=report.html --self-contained-html                 # all three + HTML report
```

Screenshots are saved to `evidence/` with the names used in the report, e.g. `TC02_S1.png`, `TC04_S2b.png`.
A failing check also saves `evidence/FAILED_<test name>.png`.
Each run creates real accounts on the demo site (`a3tester.<timestamp>@example.com`).
