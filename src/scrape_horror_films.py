from string import ascii_uppercase
import csv

import requests
import bs4

from film import Film

# Create dictionary of states for scraping Wikipedia.
with open("data/us_states.csv", 'r') as f:
    reader = csv.reader(f)
    us_states = [row[0] for row in reader]

cleaned_us_states = {}
for state in us_states:
    if state == "Georgia":
        new_state = "Georgia_(U.S._state)"
        cleaned_us_states[state] = new_state
    elif state == "New York":
        new_state = "New_York_(state)"
        cleaned_us_states[state] = new_state
    elif state == "Washington":
        new_state = "Washington_(state)"
        cleaned_us_states[state] = new_state
    elif " " in state:
        new_state = state.replace(" ", "_")
        cleaned_us_states[state] = new_state
    else:
        cleaned_us_states[state] = state

# Scraping Wikipedia for horror films released from 1960 - 2022.
horror_films = []
for year in range(1960, 2023):
    content = requests.get(
        f"https://en.wikipedia.org/wiki/List_of_horror_films_of_{year}"
    )
    soup = bs4.BeautifulSoup(content.text, "html.parser")
    film_table = soup.find("table", {"class": "wikitable sortable"})
    films = film_table.find_all("i")
    for film in films:
        film_object = Film(film.text, str(year))
        horror_films.append(film_object)

# Scrape Wikipedia for which films are set in which US states.
states_films = []
for state, URL_parameter in cleaned_us_states.items():
    print(URL_parameter)
    for letter in ascii_uppercase:
        content = requests.get(
            f"https://en.wikipedia.org/w/index.php?title=Category:Films_set_in_{URL_parameter}&from={letter}"
        )
        soup = bs4.BeautifulSoup(content.text, "html.parser")
        film_table = soup.find(
            "div", {"lang": "en", "dir": "ltr", "class": "mw-content-ltr"}
        )
        films = film_table.find_all("li")
        for film in films:
            film_object = Film(film.text, setting=state)
            if film_object in states_films:
                other_film_object_index = states_films.index(film_object)
                other_film_object = states_films[other_film_object_index]
                # Check to see if it's a film produced in a different year.
                if film_object.year_released is not None and \
                other_film_object.year_released is not None and \
                film_object.year_released != other_film_object.year_released:
                    states_films.insert(0, film_object) # To ensure next object with same title is compared against most recent object.
                else:
                    film_object.setting = other_film_object.setting
                    film_object.setting.add(state)
                    del states_films[other_film_object_index]
                    states_films.insert(0, film_object)
            else:
                states_films.append(film_object)

# Check to see which horror films are set in which US states.
horror_films_with_states = []
for film in states_films:
    if film in horror_films and film.year_released is None:
        film.year_released = horror_films[horror_films.index(film)].year_released
        horror_films_with_states.append(film)
    elif film in horror_films and film.year_released is not None:
        horror_films_with_states.append(film)

# Writing results to CSV file.
with open("data/horror_films.csv", "w") as file_object:
    writer = csv.DictWriter(file_object, fieldnames=["Film", "Year released",
    "Setting"])
    writer.writeheader()
    for film in horror_films_with_states:
        for location in film.setting:
            writer.writerow(
            {
                "Film": film.title,
                "Year released": film.year_released,
                "Setting": location
            }
            )

