import time
import requests
import cloudscraper

from bs4 import BeautifulSoup
import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome
from selenium.webdriver.support import expected_conditions as EC


# The website is under cloudflare protection.
# https://steamdb.info/graph/ is using Cloudflare CDN/Proxy!
# https://steamdb.info/graph/ is using Cloudflare SSL!

# So use cloudflare scrapping or undetected scrapping to avoid getting blocked

prefs = {
    "detach":True
}
options = uc.ChromeOptions()
options.add_experimental_option("prefs", prefs)
options.headless = False


driver = Chrome(options=options)
driver.maximize_window()
url = "https://steamdb.info/charts/"
driver.get(url)

WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="table-apps_length"]/label/select'))).click()
WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="table-apps_length"]/label/select/option[7]'))).click()

data = driver.page_source

soup = BeautifulSoup(data,"html.parser")
content = soup.find_all("tr","app")

values = []
for i in content:
    values.append(i.text)


values_new = []
for i in range(len(values)):
    a = values[i].replace("\n", ";")
    a = a.replace("+", "\n")
    a = a.replace(";;", ";")
    a = a.replace(";\n;", "\n")
    a = a.replace(f";{i+1}.",f"{i+1}.")
    values_new.append(a)
print(values_new)


with open("top games.csv","a", encoding="utf-8") as writetofile:
    writetofile.write('No;Name;Current;24hPeak;All Time Peak\n')
    for i in values_new:
        writetofile.write(i)
