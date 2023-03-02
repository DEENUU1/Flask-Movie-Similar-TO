from requests import get
from dotenv import load_dotenv
import os
import json
from dataclasses import dataclass
from typing import List, Dict, Any


load_dotenv()


class SearchMovie:
    """ This class allows to get movie ID """

    def __init__(self, query: str):
        self.api_key = os.getenv('MOVIEDB_API_KEY')
        self.query = query

    def create_query(self) -> str:
        """ This method format the user input into query """
        query_list = self.query.lower().split()
        return '-'.join(query_list)

    @property
    def return_movie_id(self):
        """ This method returns user movie ID """
        base_url = "https://api.themoviedb.org/3/search/movie?api_key="
        result = get(base_url + self.api_key + "&query=" + self.create_query())
        json_result = json.loads(result.content)
        movie = json_result['results']

        if result.status_code == 200:
            return str(movie[0]['id'])
        else:
            raise Exception("Error")


@dataclass()
class SimilarMovieData:
    title: str
    overview: str
    release_date: str
    poster: str


class SimilarMovies:

    def __init__(self, query: str):
        self.search = SearchMovie(query)

    def search_for_similar_movies(self) -> List[Dict[str, Any]]:
        """ This method is returning json file with similar movies
            from all pages from 1 to 1000"""
        api_key = os.getenv("MOVIEDB_API_KEY")
        base_url = "https://api.themoviedb.org/3/movie/"
        all_results = []
        page_number = 1
        while True:
            response = get(
                f"{base_url}{self.search.return_movie_id}/recommendations?api_key={api_key}&page={page_number}")
            json_result = json.loads(response.content)
            if not json_result.get('results'):
                break
            all_results.extend(json_result['results'])
            page_number += 1
            if page_number > 1000:
                break
        return all_results

    def return_similar_movies(self) -> list[SimilarMovieData]:
        """ This method returns
            title, release date, overview, photo
            for all similar movies"""
        all_movies = []
        for movie in self.search_for_similar_movies():
            movie_data = SimilarMovieData(
                title=movie['title'],
                release_date=movie['release_date'][:4],
                overview=movie['overview'],
                poster=movie['poster_path']
            )
            all_movies.append(movie_data)
        return all_movies
