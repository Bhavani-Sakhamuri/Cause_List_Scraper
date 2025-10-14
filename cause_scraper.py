from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, base64
import pandas as pd
from bs4 import BeautifulSoup

CHROMEDRIVER_PATH = "E:/PythonProjects/chromedriver.exe"
url = "https://bengaluru.dcourts.gov.in/cause-list-%e2%81%84-daily-board/"  # replace with real site or open demo page

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
print("Browser opened. Solve any CAPTCHA if present, then press Enter here.")
driver.get(url)
input()

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Example: extract table rows (adjust to actual site)
rows = []
for tr in soup.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all(["td","th"])]
    if cols:
        rows.append(cols)

if rows:
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.to_csv("E:/PythonProjects/output/cause_list.csv", index=False)
    print("✅ Saved cause_list.csv")

pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
with open("E:/PythonProjects/output/cause_list.pdf", "wb") as f:
    f.write(base64.b64decode(pdf["data"]))
print("✅ Saved cause_list.pdf")

driver.quit()
