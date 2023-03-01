from requests import get
from dotenv import load_dotenv
import os
import json

load_dotenv()


def create_query(query="Mission impossible"):
    query_list = query.lower().split()
    return '-'.join(query_list)


def return_movie_id():
    api_key = os.getenv("MOVIEDB_API_KEY")
    base_url = "https://api.themoviedb.org/3/search/movie?api_key="
    result = get(base_url + api_key + "&query=" + create_query())
    json_result = json.loads(result.content)
    movie = json_result['results']

    if result.status_code == 200:
        return str(movie[0]['id'])
    else:
        raise Exception("Error")


def search_similar_movie():
    api_key = os.getenv("MOVIEDB_API_KEY")
    base_url = "https://api.themoviedb.org/3/movie/"
    result = get(base_url + return_movie_id() + "/similar?api_key=" + api_key)
    json_result = json.loads(result.content)
    similar_movies = json_result['results']

    if result.status_code == 200:
        return [movie for movie in similar_movies]
    else:
        raise Exception("Error")

print(search_similar_movie())