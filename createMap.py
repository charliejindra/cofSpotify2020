import pandas as pd 
import matplotlib.pyplot as plt 
import geopandas as gpd 

while True:
    choices = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo"
    ]

    print('What map do you wanna see?')
    print(
        'Danceability(1)\n'
        'Energy(2)\n'
        'Loudness(3)\n'
        'Speechiness(4)\n'
        'Acousticness(5)\n'
        'Instrumentalness(6)\n'
        'Liveness(7)\n'
        'Valence(8)\n'
        'Tempo(9)\n'
        '--------------------------'
    )
    choice_map = input()

    choice_key = input('How much do you want the data to be sectioned? (May not be exact): ')

    revenue = pd.read_excel(choices[int(choice_map) - 1] + '.xlsx')

    # GETS WORLD LOCATIONS, NAMES, AND 3 DIGIT WORLD NUMBERS
    world = world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


    for_plotting = world.merge(revenue, left_on = 'iso_a3', right_on = 'Country Code')

    ax = for_plotting.plot(column='data', cmap='YlGnBu', figsize=(15,9), scheme='quantiles', k=int(choice_key), legend=True)

    plt.show()

    go_again = input("Would you like to go again (y/n): ")
    if go_again != 'y':
        break 
    