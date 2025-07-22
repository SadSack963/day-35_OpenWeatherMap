# pip install requests python-dotenv requests-cache
import requests
from dotenv import load_dotenv
import os
import requests_cache

# Create an SQL database to limit API calls
requests_cache.install_cache("weather_cache", expire_after=3600)

load_dotenv("D:/Python/EnvironmentVariables/.env")
APP_ID = os.environ.get("APIKey-OpenWeatherMap-Python")


def geo_location(city: str, country_code: str = None) -> tuple[float, float, str]:
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
        'limit': 10,
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


def geo_zip(zip_code: str, country_code: str = None) -> tuple[float, float, str]:
    """
    Get geographical coordinates by ZIP or Postcade
    Country Codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

    :param zip_code: ZIP or Postcade to search for
    :type zip_code: str
    :param country_code: Country to search in (optional)
    :type country_code: str
    :return: lattitude, longitude, country code
    :rtype: tuple[float, float, str]
    """
    url = "http://api.openweathermap.org/geo/1.0/zip"
    query = f'{zip_code}'
    if country_code:
        query += f',{country_code}'
    params = {
        'zip': query,
        'appid': APP_ID,
    }
    response = requests.get(url=url, params=params)
    # print(response.text)
    """
    {
      "zip":"NN10",
      "name":"Wymington",
      "lat":52.2688,
      "lon":-0.6027,
      "country":"GB"
    }
    """
    response.raise_for_status()
    first_result = response.json()
    return first_result["lat"], first_result["lon"], first_result["country"]


def geo_reverse(lat: float, lon: float) -> str:
    """
    Get location name from geographical coordinates

    :param lat: Latitude to search for
    :type lat: float
    :param lon: Longitude to search for
    :type lon: float
    :return: Location name
    :rtype: str
    """
    url = "http://api.openweathermap.org/geo/1.0/reverse"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': APP_ID,
        'limit': 1,
    }
    response = requests.get(url=url, params=params)
    # print(response.text)
    """
    [
      {
        "name":"Shire Of Donnybrook-Balingup",
        "local_names":{
          "en":"Shire Of Donnybrook-Balingup"
        },
        "lat":-33.7022605,
        "lon":115.99736970337452,
        "country":"AU",
        "state":"Western Australia"
      }
    ]
    """
    response.raise_for_status()
    city = response.json()[0]["name"]
    return city


if __name__ == '__main__':
    # FIND LOCATION BY CITY NAME
    lat, lon, code = geo_location("Perth")
    print(lat, lon, code)
    lat, lon, code = geo_location("Perth", "gb")
    print(lat, lon, code)

    # FIND LOCATION BY ZIP / POSTCODE
    lat, lon, code = geo_zip("6239", "au")
    print(lat, lon, code)
    lat, lon, code = geo_zip("NN10", "gb")
    print(lat, lon, code)

    # FIND LOCATION NAME FROM COORDINATES
    city_name = geo_reverse(51.5128, -0.0918)
    print(city_name)
    city_name = geo_reverse(-33.5622, 115.8524)
    print(city_name)
