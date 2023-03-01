from requests import get
from dotenv import load_dotenv
import os
import json

load_dotenv()


def create_query(query="Ant man and the wasp"):
    query_list = query.lower().split()
    return '-'.join(query_list)


def return_data():
    api_key = os.getenv("MOVIEDB_API_KEY")
    base_url = f"https://api.themoviedb.org/3/search/movie?api_key="
    result = get(base_url + api_key + "&query=" + create_query())
    json_result = json.loads(result.content)
    print(base_url + api_key + "&query=" + create_query())
    return json_result


print(return_data())