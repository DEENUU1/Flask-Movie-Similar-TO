import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any

from dotenv import load_dotenv
from requests import get
from functools import lru_cache

load_dotenv()


@dataclass()
class ShowData:
    """ This dataclass allows to represent data from the API """
    title: str
    overview: str
    release_date: str
    poster: str


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
    @lru_cache(maxsize=128)
    def return_id(self) -> str:
        """ This method returns user movie ID """
        base_url = f"https://api.themoviedb.org/3/search/{self.type}?api_key="
        result = get(base_url + self.api_key + "&query=" + self.create_query())
        json_result = json.loads(result.content)
        data = json_result['results']

        if result.status_code == 200:
            try:
                return str(data[0]['id'])
            except KeyError:
                return "None"
        else:
            raise Exception(f"Status code {result.status_code}")


class Similar:
    """ This class allows to return similar movies and tv shows from the API """
    def __init__(self, query: str, type: str):
        self.search = Search(query, type)
        self.type = type
        self.api_key = os.getenv("MOVIEDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3/"

    @lru_cache(maxsize=128)
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

    @lru_cache(maxsize=128)
    def return_similar_shows(self) -> list[ShowData]:
        """ This method returns
            title, date release, overview, photo
            for all similar movies and tv shows """

        if self.type == "movie":
            all_movies = []
            for movie in self.search_for_similar():
                shows_data = ShowData(
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
                show_data = ShowData(
                    title=show['name'],
                    release_date=show['first_air_date'][:4],
                    overview=show['overview'],
                    poster=show['backdrop_path']
                )
                all_tv_shows.append(show_data)
            return all_tv_shows


class BaseAPI:
    """ Base class that allows to make request to API
        and return data from all API pages """
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.api_key = os.getenv("MOVIEDB_API_KEY")

    def _get_data(self, page: int = 1) -> List[Dict[str, Any]]:
        """ This method allows to make request to the API """
        response = get(f"{self.endpoint}?api_key={self.api_key}&page={page}")
        json_result = json.loads(response.content)
        if not json_result.get('results'):
            return []
        return json_result['results']

    def return_data(self, page: int = 1) -> List[ShowData]:
        """ This method allows to return data from the API and display them in the flask view """
        all_data = []
        for data in self._get_data(page=page):
            data_object = ShowData(
                title=data['title'],
                overview=data['overview'],
                poster=data['poster_path'],
                release_date=data['release_date']
            )
            all_data.append(data_object)
        return all_data


class UpComingMovies(BaseAPI):
    """ This class inherits from BaseAPI and allows to return all upcoming movies """
    def __init__(self):
        endpoint = "https://api.themoviedb.org/3/movie/now_playing"
        super().__init__(endpoint=endpoint)


class PopularMovies(BaseAPI):
    """ This class inherits from BaseAPI and allows to return all popular movies """
    def __init__(self):
        endpoint = "https://api.themoviedb.org/3/movie/popular"
        super().__init__(endpoint=endpoint)

