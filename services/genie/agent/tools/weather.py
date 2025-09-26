from langchain_core.tools import tool
import requests

@tool
def weather_search(city: str) -> str:
    """
    Description:
        Search the weather for a specific city.
    Parameters:
        city (str): The city to search the weather for
    """ 
    request = requests.get(f"https://api.weather.gov/points/{city}")
    return request.json()
