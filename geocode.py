# pip install requests python-dotenv requests-cache
import requests
from dotenv import load_dotenv
import os
import requests_cache

# Create an SQL database to limit API calls
requests_cache.install_cache("weather_cache", expire_after=3600)

load_dotenv("D:/Python/EnvironmentVariables/.env")
APP_ID = os.environ.get("APIKey-OpenWeatherMap-Python")


def geo_location(city, country_code=None):
    """
    Get geographical coordinates by location name
    Country Codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

    :param city: City to search for
    :type city: str
    :param country_code: Country to search in (optional)
    :type country_code: str
    :return: lattitude, longitude, country code
    :rtype: tuple[float, float, str]
    """
    url = "http://api.openweathermap.org/geo/1.0/direct"
    query = f'{city}'
    if country_code:
        query += f',{country_code}'
    params = {
        'q': query,
        'appid': APP_ID,
        'limit': 1,
    }
    response = requests.get(url=url, params=params)
    # print(response.text)
    """
    Example Response
    [
      {
        "name":"Milton Keynes",
        "local_names":{
          "ur":"ملٹن کینز",
          "en":"Milton Keynes",
          "ru":"Милтон-Кейнс"
        },
        "lat":52.0406502,
        "lon":-0.7594092,
        "country":"GB",
        "state":"England"
      }
    ]
    """
    response.raise_for_status()
    first_result = response.json()[0]
    return first_result["lat"], first_result["lon"], first_result["country"]


if __name__ == '__main__':
    lat, lon, code = geo_location("Perth")
    print(lat, lon, code)
    lat, lon, code = geo_location("Perth", "gb")
    print(lat, lon, code)
