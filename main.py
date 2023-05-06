import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def scrape(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    elements = driver.find_elements(By.CSS_SELECTOR, '.ui-li-heading.text2share, .text2share:not(.next)')

    menu_items = []
    for element in elements:
        item_text = element.text.strip().replace('­', '')
        item_text = re.sub(r'\(.*\)', '', item_text)
        if item_text:
            menu_items.append(item_text)

    driver.quit()

    return menu_items


if __name__ == '__main__':
    url = 'https://oldenburg.my-mensa.de/essen.php?v=5611274&hyp=1&lang=de&mensa=uh#uh_tag_1'
    menu = scrape(url)
    for item in menu:
        print(item)
