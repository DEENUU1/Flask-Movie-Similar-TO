import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any

from dotenv import load_dotenv
from requests import get

load_dotenv()


class Search:
    """ This class allows to get movie ID """

    def __init__(self, query: str, type: str):
        self.api_key = os.getenv('MOVIEDB_API_KEY')
        self.query = query
        self.type = type

    def create_query(self) -> str:
        """ This method format the user input into query """
        query_list = self.query.lower().split()
        return '-'.join(query_list)

    @property
    def return_id(self) -> str:
        """ This method returns user movie ID """
        base_url = f"https://api.themoviedb.org/3/search/{self.type}?api_key="
        result = get(base_url + self.api_key + "&query=" + self.create_query())
        json_result = json.loads(result.content)
        data = json_result['results']

        if result.status_code == 200:
            return str(data[0]['id'])
        else:
            raise Exception("Error")


@dataclass()
class SimilarData:
    title: str
    overview: str
    release_date: str
    poster: str


class Similar:
    def __init__(self, query: str, type: str):
        self.search = Search(query, type)
        self.type = type
        self.api_key = os.getenv("MOVIEDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3/"

    def search_for_similar(self) -> List[Dict[str, Any]]:
        """ This method is searching for similar tv shows or movies """
        all_results = []
        page_number = 1
        while True:
            response = get(
                f"{self.base_url}{self.type}/{self.search.return_id}/recommendations?api_key={self.api_key}&page={page_number}")
            json_result = json.loads(response.content)
            if not json_result.get('results'):
                break
            all_results.extend(json_result['results'])
            page_number += 1
            if page_number > 1000:
                break
        return all_results

    def return_similar_shows(self) -> list[SimilarData]:
        """ This method returns
            title, date release, overview, photo
            for all similar movies and tv shows """

        if self.type == "movie":
            all_movies = []
            for movie in self.search_for_similar():
                shows_data = SimilarData(
                    title=movie['title'],
                    release_date=movie['release_date'][:4],
                    overview=movie['overview'],
                    poster=movie['poster_path']
                )
                all_movies.append(shows_data)
            return all_movies

        elif self.type == 'tv':
            all_tv_shows = []
            for show in self.search_for_similar():
                show_data = SimilarData(
                    title=show['name'],
                    release_date=show['first_air_date'][:4],
                    overview=show['overview'],
                    poster=show['backdrop_path']
                )
                all_tv_shows.append(show_data)
            return all_tv_shows


@dataclass()
class UpComingData:
    title: str
    poster: str
    overview: str
    release_date: str


class UpComingMovies:
    def __init__(self):
        self.api_key = os.getenv("MOVIEDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3/movie/now_playing"

    def search_upcoming_movies(self, page: int = 1) -> List[Dict[str, Any]]:
        """This method searches for upcoming movies available in cinema
        on a specific page and with a specific number of results per page"""
        response = get(
            f"{self.base_url}?api_key={self.api_key}&page={page}")
        json_result = json.loads(response.content)
        if not json_result.get('results'):
            return []
        return json_result['results']

    def return_upcoming_movies(self, page: int = 1) -> List[UpComingData]:
        """ This method allows returning data from the API about upcoming movies
         on a specific page and with a specific number of results per page"""
        all_upcoming = []
        for upcoming in self.search_upcoming_movies(page=page):
            upcoming_data = UpComingData(
                title=upcoming['title'],
                overview=upcoming['overview'],
                poster=upcoming['poster_path'],
                release_date=upcoming['release_date']
            )
            all_upcoming.append(upcoming_data)
        return all_upcoming
