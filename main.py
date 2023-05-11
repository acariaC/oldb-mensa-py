# This script fetches https://oldenburg.my-mensa.de/essen.php?v=5611274&hyp=1&lang=de&mensa=uh#uh_tag_1
# using urrlib3 and parses the HTML using BeautifulSoup. It then prints the menu items to the console.

import re
import urllib3
from bs4 import BeautifulSoup
import json
import os
from flask import Flask
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def scrape(data="", ausgabe="ausgabe-eins", date="2023-05-08"):
    # Parse HTML
    soup = BeautifulSoup(data, 'html.parser')

    # Filter for containg data-date2="2023-05-08"
    elements = soup.find_all(attrs={'data-date2': re.compile(date)})

    # Filter li class="conditional ausgabe-eins checkempty"
    # String format, ausgabe as variable
    compile_string = "conditional {ausgabe} checkempty".format(ausgabe=ausgabe)
    elements = [element.find_all(class_=re.compile(compile_string)) for element in elements]

    # Filter out prices using filter class ct next text2share
    prices = [[item.find(class_='ct next text2share') for item in element] for element in elements]

    # Extract text from prices
    prices = [[item.get_text() for item in element] for element in prices]

    # Filter out each item with class="text2share"
    elements = [[item.find(class_='text2share') for item in element] for element in elements]

    # Extract text from elements
    elements = [[item.get_text() for item in element] for element in elements]

    # Remove \xad from elements list
    elements = [[item.replace('­', '') for item in element] for element in elements]

    # Filter out things like \xad from prices
    prices = [[item.replace('\xad', '') for item in element] for element in prices]
    # Filter out things like \xa0 from prices
    prices = [[item.replace('\xa0', '') for item in element] for element in prices]

    # Create map of menu items and prices
    menu_items = dict(zip(elements[0], prices[0]))

    return menu_items


def scrape_mensa():
    url = 'https://oldenburg.my-mensa.de/essen.php?v=5611274&hyp=1&lang=de&mensa=uh#uh_tag_1'

    # Set agent to Firefox
    http = urllib3.PoolManager(headers={'User-Agent': 'Mozilla/5.0'})
    response = http.request('GET', url)

    # Save response as html file
    with open('output/response.html', 'wb') as f:
        f.write(response.data)

    # Extract all dates from HTML as list in format yyyy-mm-dd
    soup = BeautifulSoup(response.data, 'html.parser')
    dates = soup.find_all(attrs={'data-date2': re.compile(r'\d{4}-\d{2}-\d{2}')})
    dates = [date['data-date2'] for date in dates]

    # Scrape all dates
    for date in dates:
        # Scrape all ausgaben, save as json using date as filename, format yyyy-mm-dd.json
        # Each json contains a map of menu items and prices
        # Level 0: Name of ausgabe
        # Level 1: Name of menu item and price as list
        ausgaben = ['ausgabe-eins', 'ausgabe-zwei', 'ausgabe-drei', 'suppe', 'beilagen', 'salate', 'desserts',
                    'culinarium-hauptgerichte', 'culinarium-beilagen', 'culinarium-desserts', 'culinarium-salate']

        # Combine all ausgaben into one json later
        ausgaben_stored = {}
        for ausgabe in ausgaben:
            ausgaben_stored[ausgabe] = scrape(response.data, ausgabe, date)

        # Create output folder if not exists
        if not os.path.exists('output'):
            os.makedirs('output')

        # Save as json
        with open('output/{date}.json'.format(date=date), 'w') as outfile:
            json.dump(ausgaben_stored, outfile)


# Publish json files from output folder using Flask
app = Flask(__name__)


def send_from_directory(directory, path):
    return open(os.path.join(directory, path)).read()


# resource to get data from current day, return empty json if not exists
@app.route('/api/v1/mensa')
def get_mensa():
    # Get current date
    import datetime
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # Check if file exists
    if os.path.exists('output/{date}.json'.format(date=date)):
        return send_from_directory('output', '{date}.json'.format(date=date))
    else:
        return json.dumps({})


@app.route('/api/v1/mensaPlain')
def get_mensaPlain():
    import datetime
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    if os.path.exists('output/{date}.json'.format(date=date)):
        with open('output/{date}.json'.format(date=date), encoding="utf-8") as file:
            data = json.load(file)

        menu = []
        for outer_key, outer_value in data.items():
            # print(outer_key)
            menu.append(outer_key)

            for inner_key in outer_value.keys():
                # print(inner_key)
                menu.append(inner_key)
            # print()


        return menu
    else:
        return json.dumps({})

# resource to get data from specific day, return empty json if not exists

@app.route('/api/v1/mensa/<date>')
def get_mensa_date(date):
    # Check if file exists
    if os.path.exists('output/{date}.json'.format(date=date)):
        return send_from_directory('output', '{date}.json'.format(date=date))
    else:
        return json.dumps({})


cron = BackgroundScheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()


# Run every hour
@cron.scheduled_job('interval', minutes=1)
def job_function():
    print("Scraping mensa")
    scrape_mensa()


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
