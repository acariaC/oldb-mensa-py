from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = 'https://oldenburg.my-mensa.de/essen.php?v=5611274&hyp=1&lang=de&mensa=uh#uh_tag_1'

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
webdriver = webdriver.Chrome(options=options)

webdriver.get(url)
h3_elements = webdriver.find_elements(By.CSS_SELECTOR, 'h3')

for h3_element in h3_elements:
    h3_content = h3_element.text.strip().replace('­', '')
    if len(h3_content) > 0:
        print(h3_content)

webdriver.quit()
