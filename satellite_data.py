"""
satellite_data.py

This module provides functions to fetch satellite information (NORAD) from the Celestrak website,
including a list of satellites and their Two-Line Element (TLE) data.

Dependencies:
- ephem: Python library for performing high-precision astronomy computations.
- requests: Python library for making HTTP requests.

Author: akelly
Date: 1/30/2024
"""
import requests
import os

# Cache Ephemeris Data (this is useful for when we aren't able to connect to the internet)
CACHE_FILE = "ephemeris_cache.txt"

def has_internet_connection():
    """
    Check if there is an active internet connection by attempting to connect to a site that typically works.
    I chose https://www.google.com.

    Returns:
        bool: True if connection is established, False if connection not established.
    """
    try:
        # Try to make a simple HTTP request to a known website
        response = requests.get("https://www.google.com", timeout=5)
        # Return True if the response.status_code == 200 for a successful connection
        return response.status_code == 200
    except requests.ConnectionError:
        # If there is a connection error, return False
        return False

def fetch_satellite_list(url, CACHE_FILE=CACHE_FILE):
    """
    Fetch a list of satellites from the input URL, cache it locally, and return the data.

    If an internet connection is available, it fetches the data from online and saves it to the cached file.
    If no internet connection is reached, then use the cached data.

    Args:
        url (str): The URL to fetch the data

    Returns:
        list: List of tuples containing satellite names and NORAD catalog numbers.
    """
    # Check for an internet connection to determine whether to use cached data
    if has_internet_connection():
        # Fetch data from online
        response = requests.get(url)
        tle_data = response.text.splitlines()

        # Save data to the cache
        with open(CACHE_FILE, "w") as file:
            file.writelines(f"{line}\n" for line in tle_data)

    # Read from the file for cached data if there is no internet connection
    elif os.path.exists(CACHE_FILE):
        # Load data from cache
        with open(CACHE_FILE, "r") as file:
            tle_data = [line.strip() for line in file.readlines()]

    # Initialize an empty list to store the satellite information
    satellites = []

    # Each satellite has 3 lines of data
    for i in range(0, len(tle_data), 3):
        name, catalog_line, _ = tle_data[i:i + 3]
        catalog_number = catalog_line.split()[1]
        # Append the tuple containing the satellite name and catalog number to the satellites list
        satellites.append((name, catalog_number))

    return satellites

def get_tle_data(selected_satellites):
    """
    Fetch TLE data for the selected satellites from the Celestrak website.

    Parameters:
        selected_satellites (list): List of tuples containing satellite names and NORAD catalog numbers.

    Returns:
        list: List of TLE data for the selected satellites.
    """
    with open(CACHE_FILE, "r") as file:
        tle_data = [line.strip() for line in file.readlines()]

    selected_tle_data = []
    for satellite in selected_satellites:
        for i in range(0, len(tle_data), 3):
            catalog_number = tle_data[i + 1].split()[1]
            if catalog_number == satellite[1]:
                selected_tle_data.append(tle_data[i:i + 3])
                break

    return selected_tle_data
