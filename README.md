# oldb-mensa-py

Webscraping application for getting todays menu at 'Mensa Uhlhornsweg' at Carl-von-Ossietzky Universität Oldenburg. 

## API Endpoints
* `api/v1/mensa` - returns the menu for today
* `api/v1/mensaPlain` - returns the menu for today as a list of Strings
* `api/v1/mensa/<date>` - returns the menu for the given date, using the format `YYYY-MM-DD`

## TBD:
 - make sure that Siri can access the output through a shortcut
 - add special alerts for personal favorite menu items
 - add selection within Terminal for 'Uhlhornsweg', 'Wechloy'
