"""
ReZAKORA-Bypass Test Script
"""

from patchright.sync_api import sync_playwright
from ReZakoraSolver import ReZAKORASolver

URL = "https://www.google.com/recaptcha/api2/demo"

def main():
    print("=" * 50)
    print("ReZAKORA-Bypass - reCAPTCHA Solver Test")
    print("=" * 50)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded")
        
        solver = ReZAKORASolver(page)
        try:
            solver.solve()
            print("Solved [OK]")
        except Exception as e:
            print(f"FAILED: {e}")
        
        browser.close()

if __name__ == "__main__":
    main()
