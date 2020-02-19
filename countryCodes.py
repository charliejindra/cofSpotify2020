import requests 
from bs4 import BeautifulSoup


def getData():
    page = requests.get("https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2")
    soup = BeautifulSoup(page.content, 'html.parser')

    countries_available = [     # Places where Spotify is available
        'Algeria','Egypt','Morocco','South Africa','Tunisia',
    'Bahrain','Hong Kong','India','Indonesia','Israel','Japan','Jordan','Kuwait','Lebanon','Malaysia','Oman','Palestine','Philippines','Qatar','Saudi Arabia','Singapore','Taiwan','Thailand','United Arab Emirates','Vietnam',
    'Andorra','Austria','Belgium','Bulgaria','Cyprus','Czech Republic','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Iceland','Ireland','Italy','Latvia','Liechtenstein','Lithuania','Luxembourg','Malta','Monaco','Netherlands','Norway','Poland','Portugal','Romania','Slovakia','Spain','Sweden','Switzerland','Turkey','United Kingdom',
    'Canada','Costa Rica','Dominican Republic','El Salvador','Guatemala','Honduras','Mexico','Nicaragua','Panama','United States',
    'Argentina','Bolivia','Brazil','Chile','Colombia','Ecuador','Paraguay','Peru','Uruguay',    
    ]

    tables = soup.find_all('table')
    wanted_table = tables[2]    # Wanted table is the officially assigned code elements

    rows = wanted_table.find_all('tr')
    country_codes = {}

    for row in rows:
        data = row.find_all('td')

        if len(data) != 0:
            for country in countries_available: # can delete this if looking at every country in the world
                if data[1].text == country:     # not all countries have spotify so checks if the country is available
                    country_codes.update({data[0].text: data[1].text}) 

    return country_codes 


print(getData())