
# Movie Similar To

An application that allows you to search for similar movies or TV series. And also allows you to browse popular movies and upcoming premieres.
The user can save the videos to his profile.

<img src="/images/app.gif"/>


## Demo

- [LIVE DEMO](https://deenuu1.pythonanywhere.com/)
- [YOUTUBE LINK](https://www.github.com/DEENUU1)


## The project is divided into 3 sections:

### Search for similar movies and series.
The user can enter his movie or series and then a list of similar movies will be returned to him. In this section user can add any video to his profile as "to watch" or "watched"
### List of upcoming premieres.
This section allows the user to view a list of upcoming releases. The whole is divided into many pages thanks to pagination.
### List of popular videos.
This section allows the user to view the list of the most popular videos. The whole is divided into many pages thanks to pagination.

```code
    @property
    @lru_cache(maxsize=128)
    def return_id(self) -> Union[str, None]:
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
```

Also I used @lru_cache decorator to increase efficienty of requests to the API. \
Here is some tests that I did to compere the efficienty with @lru_cache and without it.

<img src="/images/excel.png"/>


### Project is based on technologies such as:
- Python (Flash)
- HTML & Bootstrap
- Rest API

Movie data is retrieved from the API provided by themoviedb

## Installation

Clone the repository

```bash
git clone <link>
```

Install the requirements

```bash
pip install -r requirements.txt
```

Inside similar_movies folder add .env file. It should looks like this:

```bash
MOVIEDB_API_KEY=
SECRET_KEY=<SOME RANDOM CHARACTERS>
EMAIL_USERNAME=<GMAIL EMAIL>
EMAIL_PASSWORD=<GMAIL PASSWORD>
```


Key api you can get here: https://www.themoviedb.org/documentation/api \
Password for your Gmail account you can get here: https://bit.ly/3lj3dhQ 

Run the application by using this command

```bash
python main.py 
```
## Running Tests

To run tests, run the following command

```bash
  pytest
```


## Authors

- [@DEENUU1](https://www.github.com/DEENUU1)

