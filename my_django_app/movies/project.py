# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 16:20:48 2021

@author: daggy
"""



#plik główny


import requests
import pandas as pd
import numpy as np

tytuly2 = ['The Shawshank Redemption',
'Memento',
'In Bruges',
'Gods',
'The Godfather',
'The Dark Knight',
'12 Angry Men',
'Gone Girl',
'Pulp Fiction',
'Fight Club',
'Forrest Gump',
'Joker',
'Inception',
'The Matrix',
'Goodfellas',
'Seven Samurai',
'Se7en',
'City of God',
'Seven Pounds',
'Boyhood',
'Contratiempo',
'Vicky Cristina Barcelona',
'The Silence of the Lambs',
'The Silence of the Lambs',
'Saving Private Ryan',
'The Green Mile ',
'Interstellar',
'The Usual Suspects',
'The Lion King',
'Back to the Future',
'The Pianist',
'The Intouchables',
'Psycho',
'Gladiator',
'City Lights',
'The Departed',
'Whiplash',
'The Prestige',
'Casablanca',
'Cinema Paradiso',
'Alien',
'Apocalypse Now',
'Django Unchained',
'The Shining',
'Parasite',
'Oldboy',
'The Dark Knight Rises',
'American Beauty',
'Coco',
'Braveheart',
'Toy Story',
'Amadeus',
'Inglourious Basterds',
'Good Will Hunting',
'Requiem for a Dream',
'Vertigo',
'Eternal Sunshine of the Spotless Mind',
'Citizen Kane',
'The Hunt',
'Enemy at the Gates',
'Full Metal Jacket',
'A Clockwork Orange',
'Snatch',
'Scarface',
'Lawrence of Arabia',
'Taxi Driver',
'The Sting',
'To Kill a Mockingbird',
'Indiana Jones and the Last Crusade',
'Ben Hur',
'The Apartment',
'Incendies',
'Heat',
'Batman Begins',
'Die Hard',
'Unforgiven',
'Green Book',
'Children of Heaven',
'Downfall',
'A Beautiful Mind',
'Raging Bull',
'The Wolf of Wall Street',
'Chinatown',
'The Gold Rush',
'Inside Out',
'There Will Be Blood',
'Gran Torino',
'Warrior',
'Room',
'Shazam',
'Trainspotting',
'No Country for Old Men',
'The Sixth Sense',
'Shutter Island',
'The Thing',
'Jurassic Park',
'Blade Runner',
'Gone with the Wind',
'The Big Lebowski',
'Fargo']

def titles():
    tableoftitles = []
    for elem in tytuly2:
      tableoftitles.append(elem.replace(' ', '+'))
    return tableoftitles

tableoftitles = titles()


def getmovieinfo(tableoftitles):
    
    title = 'Title":"'
    year = '"Year":"'
    runtime = '"Runtime":"'
    genre = '"Genre":"'
    director = '"Director":"'
    cast = '"Actors":"'
    country = '"Country":"'
    awards = '"Awards":"'
    imdb_ratings = '"imdbRating":"'
    imdb_votes = '"imdbVotes":"'
    box_office = '"BoxOffice":"'
    
    tableOfMovies = []
    
    for elem in tableoftitles:
        path = "http://www.omdbapi.com/?t="+elem+"&apikey=7d325b17"
        response = requests.get(path)
        resp = response.text
        resp_s = resp.replace('{', '').replace('}', '').split('""')
        
        table=[]
        
        for elem in resp_s:
            title_start = elem.find(title) + len(title)
            title_end = elem.index('"', title_start)
            movie_title = elem[title_start:title_end]
        
        for elem in resp_s:
            year_start = elem.find(year) + len(year)
            year_end = elem.index('"', year_start)
            movie_year = elem[year_start:year_end]
        
        for elem in resp_s:
            runtime_start = elem.find(runtime) + len(runtime)
            runtime_end = elem.index('"', runtime_start)
            movie_runtime = elem[runtime_start:runtime_end].replace('min', '').strip()
        
        for elem in resp_s:
            genre_start = elem.find(genre) + len(genre)
            genre_end = elem.index('"', genre_start)
            movie_genre = elem[genre_start:genre_end]
        
        for elem in resp_s:
            director_start = elem.find(director) + len(director)
            director_end = elem.index('"', director_start)
            movie_director = elem[director_start:director_end]
        
        for elem in resp_s:
            cast_start = elem.find(cast) + len(cast)
            cast_end = elem.index('"', cast_start)
            movie_cast = elem[cast_start:cast_end]
        
        for elem in resp_s:
            country_start = elem.find(country) + len(country)
            country_end = elem.index('"', country_start)
            movie_country = elem[country_start:country_end]
        
        for elem in resp_s:
            awards_start = elem.find(awards) + len(awards)
            awards_end = elem.index('"', awards_start)
            movie_awards = elem[awards_start:awards_end]
        
        for elem in resp_s:
            imdb_ratings_start = elem.find(imdb_ratings) + len(imdb_ratings)
            imdb_ratings_end = elem.index('"', imdb_ratings_start)
            movie_imdb_ratings = elem[imdb_ratings_start:imdb_ratings_end].replace(',','')
        
        for elem in resp_s:
            imdb_votes_start = elem.find(imdb_votes) + len(imdb_votes)
            imdb_votes_end = elem.index('"', imdb_votes_start)
            movie_imdb_votes = elem[imdb_votes_start:imdb_votes_end].replace(',','')
        
        for elem in resp_s:
            box_office_start = elem.find(box_office) + len(box_office)
            box_office_end = elem.index('"', box_office_start)
            movie_box_office = elem[box_office_start:box_office_end].replace('$','').replace(',','')
        
        table.append(movie_title)
        table.append(movie_year)
        table.append(movie_runtime)
        table.append(movie_genre)
        table.append(movie_director)
        table.append(movie_cast)
        table.append(movie_country)
        table.append(movie_awards)
        table.append(movie_imdb_ratings)
        table.append(movie_imdb_votes)
        table.append(movie_box_office)
   
        tableOfMovies.append(table)
           
    return tableOfMovies



df = pd.DataFrame(np.array(getmovieinfo(tableoftitles)), columns = ['title','year','runtime','genre','director','actors','country','awards','imdb_ratings','imdb_votes','box_office'])
