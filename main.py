"""
main.py

This script demonstrates signal trilateration using satellite distances.
It fetches a list of satellites from the Celestrak website, allows the user to select three satellites,
retrieves their TLE data, and performs trilateration to estimate the signal origin.

Dependencies:
- ephem: Python library for performing high-precision astronomy computations.
- requests: Python library for making HTTP requests.
- ephem_trilateration: Module providing trilateration functions.
- satellite_data: Module providing functions to fetch satellite information.

Author: akelly
Date: 1/30/2024
"""
import ephem
import logging
from ephem_trilateration import trilaterate_signal_origin, plot_satellites_and_signal_origin
from satellite_data import fetch_satellite_list, get_tle_data

logging.basicConfig(level=logging.DEBUG)

def main():
    """
    Main function to demonstrate signal trilateration using satellite distances.
    """
    try:
        # The observer is set to be in Huntsville, AL for now (I just chose something here.)
        observer = ephem.Observer()
        observer.lat = '34.7304'    # Latitude of the observer's location
        observer.lon = '-86.5861'   # Longitude of the observer's location
        observer.elev = 200         # Elevation in meters (adjust as needed)

        # Fetch the satellite list from satellite_data to prompt the user to choose 3 satellites
        satellite_list = fetch_satellite_list(url = "https://www.celestrak.com/NORAD/elements/stations.txt")

        if not satellite_list:
            print("No satellites found.")
            return

        # Prompt the user to choose 3 satellites from the list for trilateration
        print("Choose three satellites for trilateration:")
        for i, (name, catalog_number) in enumerate(satellite_list, start=1):
            print(f"{i}. {name} - Catalog Number: {catalog_number}")

        # Create ephem.satellite objects to be used for trilateration
        selected_indices = [int(input(f"Enter the number corresponding to satellite {j + 1}: ")) - 1 for j in range(3)]
        selected_satellites = [satellite_list[i] for i in selected_indices]

        tle_data = get_tle_data(selected_satellites)

        satellites = [ephem.readtle(name, tle[1], tle[2]) for (name, _), tle in zip(selected_satellites, tle_data)]

        print(selected_satellites)

        tle_data = get_tle_data(selected_satellites)

        satellites = [ephem.readtle(name, tle[1], tle[2]) for (name, _), tle in zip(selected_satellites, tle_data)]

        distances = [5000.0, 6000.0, 7000.0]

        # Perform trilateration using the ephem_trilateration functions
        signal_origin = trilaterate_signal_origin(observer, *satellites, *distances)

        # Print out the lat/long of the signal origin
        if signal_origin:
            print("Estimated Signal Origin:")
            print("Latitude:", signal_origin[0])
            print("Longitude:", signal_origin[1])

        # Plot the satellites, observer, estimated signal origin, and lines indicating trilateration
        plot_satellites_and_signal_origin(satellites, signal_origin, observer)

    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()
