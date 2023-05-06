import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = 'https://oldenburg.my-mensa.de/essen.php?v=5611274&hyp=1&lang=de&mensa=uh#uh_tag_1'

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get(url)

elements = driver.find_elements(By.CSS_SELECTOR, '.ui-li-heading.text2share, .text2share:not(.next)')

for element in elements:
    element = element.text.strip().replace('­', '')
    element = re.sub(r'\(.*\)', '', element)
    if element:
        print(element)

driver.quit()
