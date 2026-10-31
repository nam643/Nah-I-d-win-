"""
Print the details Section 5 (Test Environments and Tools) asks for, and prove
that Python, Selenium, pytest and Chrome all work together.

Run inside the activated virtual environment:   python check_env.py
"""

import os
import platform
import sys

# Keep the browser inside the virtual environment: when no Chrome is installed on the system,
# Selenium Manager downloads "Chrome for Testing" and a matching ChromeDriver into
# .venv/selenium-cache/ (outside a venv: ./selenium-cache/). Deleting .venv removes both.
_IN_VENV = sys.prefix != sys.base_prefix
os.environ.setdefault(
    "SE_CACHE_PATH",
    os.path.join(sys.prefix if _IN_VENV else os.path.dirname(os.path.abspath(__file__)), "selenium-cache"),
)


def main():
    print("Operating system :", platform.platform())
    print("CPU architecture :", platform.machine())   # AMD64/x86_64 = x86-64, arm64/aarch64 = Arm64
    print("Python           :", sys.version.split()[0], "at", sys.executable)

    try:
        import pytest
        print("pytest           :", pytest.__version__)
    except ImportError:
        print("pytest           : NOT INSTALLED -> python -m pip install -r requirements.txt")

    try:
        import selenium
        print("Selenium         :", selenium.__version__)
    except ImportError:
        print("Selenium         : NOT INSTALLED -> python -m pip install -r requirements.txt")
        return

    # Start Chrome once, headless, to read the browser and driver versions.
    # The first run downloads Chrome for Testing (about 170 MB) into the venv, so it can take a minute.
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as exc:  # noqa: BLE001 - show any start-up problem plainly
        print("Chrome           : FAILED TO START ->", exc.__class__.__name__, str(exc).splitlines()[0])
        return
    caps = driver.capabilities
    print("Chrome           :", caps.get("browserVersion"), "(Chrome for Testing, kept in", os.environ["SE_CACHE_PATH"] + ")")
    print("ChromeDriver     :", caps.get("chrome", {}).get("chromedriverVersion", "?").split()[0])
    driver.get("https://opencart.abstracta.us/index.php?route=common/home")
    print("Site reachable   :", "yes" if "Your Store" in driver.title else f"unexpected title {driver.title!r}")
    driver.quit()
    print("\nAll good: you can run  pytest tests/test_tc02_registration.py")


if __name__ == "__main__":
    main()
