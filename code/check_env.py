"""
Print the details Section 5 (Test Environments and Tools) asks for, and prove
that Python, Selenium, pytest and Chrome all work together.

Run inside the activated virtual environment:   python check_env.py
"""

import platform
import sys


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

    # Start Chrome once, headless, to read the browser and driver versions
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as exc:  # noqa: BLE001 - show any start-up problem plainly
        print("Chrome           : FAILED TO START ->", exc.__class__.__name__, str(exc).splitlines()[0])
        return
    caps = driver.capabilities
    print("Chrome           :", caps.get("browserVersion"))
    print("ChromeDriver     :", caps.get("chrome", {}).get("chromedriverVersion", "?").split()[0])
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")
    print("Site reachable   :", "yes" if "Your Store" in driver.title else f"unexpected title {driver.title!r}")
    driver.quit()
    print("\nAll good: you can run  pytest tests/test_tc06_search.py")


if __name__ == "__main__":
    main()
