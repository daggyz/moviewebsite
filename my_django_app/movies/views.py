#library import to main file
from django.shortcuts import render
import requests
import pandas as pd
import numpy as np
import sqlite3



#connecting to the database, assigning the cursor and sending the query
con = sqlite3.connect('templ.db')
cur = con.cursor()
cur.execute("SELECT title FROM movies")
titles = cur.fetchall()


#declaration of the table of titles and filling it with data from the database
strTitles = []

for elem in titles:
    strTitles.append(elem[0].strip())
    
  
#breaking the connection to the database
con.commit()
con.close()


#declaration of a function that turns spaces in the title into pluses
def titles():
    tableoftitles = []
    for elem in strTitles:
      tableoftitles.append(elem.replace(' ', '+'))
    return tableoftitles

#calling a function titles() and assigning the result to a variable tableoftitles
tableoftitles = titles()


#declaration of the function getmovieinfo() responsible for connecting to omdbapi, retrieving data, preparing data (working with a string) and assigning elements to an table
def getmovieinfo(tableoftitles):

#declaration of constant result elements from omdbapi    
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
            movie_year = int(elem[year_start:year_end])
        
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
            movie_imdb_ratings = elem[imdb_ratings_start:imdb_ratings_end].replace(',','') #.replace('.', ',')#
        
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


#calling a function getmovieinfo() and assigning the result to a variable result_table
result_table = getmovieinfo(tableoftitles)


#creating a data frame df
df = pd.DataFrame(np.array(result_table), columns = ['title','year','runtime','genre','director','actors','country','awards','imdb_ratings','imdb_votes','box_office'])


#changing data types of elements in a data frame df
df['year'] = df['year'].astype(int)
df['runtime'] = df['runtime'].astype(int)
df['imdb_votes'] = df['imdb_votes'].astype(int)
df['box_office'] = df['box_office'].astype(int)


#create a copy of result_table
result_table_copy = result_table


#declaration of function sort() responsible for sorting the table according to the first element- year of production
def sort(result_table_copy):
  
    return(sorted(result_table_copy, key = lambda x: x[1])) 
   

#calling a function sort() and assigning the result to a variable result_table_sorted 
result_table_sorted = sort(result_table_copy)


#declaration of three empty tables and filling them with data from result_table_sorted
z1 = []
z2 = []
z3 = []

for elem in result_table_sorted:
    if elem[1]<1985:
        z1.append(elem)
        
    elif elem[1]>=1985 and elem[1]<2005:
        z2.append(elem)
        
    elif elem[1]>=2005:
        z3.append(elem)
        

#declaration of function dataHtml() responsible for filling empty tables with title, year, rating, votes and box office and add them to table plots_data
def dataHtml(sets):
    title_table = []

    for elem in sets:
        title_table.append(elem[0])
    
    
    year_table = []

    for elem in sets:
        year_table.append(elem[1])
    
    
    imdbratings_table = []

    for elem in sets:
        imdbratings_table.append(elem[8])
     
    
    imdbvotes_table = []

    for elem in sets:
        imdbvotes_table.append(elem[9])
      
    
    boxoffice_table = []

    for elem in sets:
        boxoffice_table.append(elem[10])
    
 
    plots_data = []
    plots_data.append(title_table)
    plots_data.append(year_table)
    plots_data.append(imdbratings_table)
    plots_data.append(imdbvotes_table)
    plots_data.append(boxoffice_table)
    
    return plots_data


#calling a function dataHtml() on three sets and assigning the result to a variables tableHTML1, tableHTML2, tableHTML3
sets = z1
tableHTML1 = dataHtml(sets)    

sets = z2
tableHTML2 = dataHtml(sets)

sets = z3
tableHTML3 = dataHtml(sets)

#assigning tableHTML1, tableHTML2, tableHTML3 to dataHTMLready
dataHTMLready=[]
dataHTMLready.append(tableHTML1)
dataHTMLready.append(tableHTML2)
dataHTMLready.append(tableHTML3)








#django views
def index(request):
    return render(request, 'index.html')


def about(request):
    my_context2 = {'about':'Something about our project and us'}
    return render(request, 'about.html', my_context2)


def contact(request):
    return render(request, 'contact.html')


def plots(request):
    my_context3 = {}
    my_context3['plots'] = dataHTMLready
    return render(request, 'plots.html', my_context3)


def random(request):
    my_context5 = {}
    string = ''
    for elem in strTitles:
        x=elem+','
        string+=x
    my_context5['random'] = string
    return render(request, 'random.html', my_context5)


def movies(request):
    alldata=[]
    for i in range(df.shape[0]):
        temp=df.iloc[i]
        alldata.append(dict(temp))
    my_context4={'movies':alldata}
    return render(request, 'movies.html', my_context4)


