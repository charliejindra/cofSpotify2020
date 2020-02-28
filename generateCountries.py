from countryCodes import getData
import os

countryFile = open("countryCodes.txt", "w")

countries = getData()
for country in countries:
    countryFile.write(country + "\n")