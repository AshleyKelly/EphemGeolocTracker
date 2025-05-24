"""
Trilateration for Signal Origin Estimation

This script performs trilateration to estimate the origin of a signal based on the distances 
from three satellites.  It utilizes the ephem library for satellite tracking, allowing the calculation 
of satellite positions, and matplotlib for visualization.

Ensure that the provided TLE (Two-Line Element) data for the satellites is up-to-date and non-colinear 
for accurate trilateration results. The script simulates a scenario where an observer, located in Huntsville, 
AL by default, measures distances to three satellites. The trilateration algorithm then determines the estimated 
latitude and longitude of the signal origin.

Author: akelly
Date: 1/30/2024
"""

import ephem
import math
import logging
import matplotlib.pyplot as plt

def trilaterate_signal_origin(observer, satellite1, satellite2, satellite3, distance1, distance2, distance3):
    """
    Trilaterate the origin of a signal using the distances from three satellites.

    Parameters:
        observer (ephem.Observer): The observer's location.
        satellite1 (ephem.satellite): The first satellite object.
        satellite2 (ephem.satellite): The second satellite object.
        satellite3 (ephem.satellite): The third satellite object.
        distance1 (float): Distance from the observer to the signal source via satellite1.
        distance2 (float): Distance from the observer to the signal source via satellite2.
        distance3 (float): Distance from the observer to the signal source via satellite3.

    Returns:
        tuple: Latitude and longitude of the estimated signal origin.
    """
    try:
        observer_lat = math.radians(observer.lat)
        observer_long = math.radians(observer.lon)

        # Ensure that the satellite positions are computed
        satellite1.compute(observer)
        satellite2.compute(observer)
        satellite3.compute(observer)

        # Calculate the unit vectors pointing from the observer to the satellites
        satellite_vector1 = ephem.Equatorial(satellite1.ra, satellite1.dec)
        satellite_vector2 = ephem.Equatorial(satellite2.ra, satellite2.dec)
        satellite_vector3 = ephem.Equatorial(satellite3.ra, satellite3.dec)

        observer_vector1 = ephem.Equatorial(observer.sidereal_time(), observer_lat)
        observer_vector2 = ephem.Equatorial(observer.sidereal_time(), observer_lat)
        observer_vector3 = ephem.Equatorial(observer.sidereal_time(), observer_lat)

        # Trilateration algorithm
        A = 2 * (satellite_vector2.ra - satellite_vector1.ra)
        B = 2 * (satellite_vector2.dec - satellite_vector1.dec)
        C = 2 * (satellite_vector3.ra - satellite_vector1.ra)
        D = 2 * (satellite_vector3.dec - satellite_vector1.dec)

        E = (distance2**2 - distance1**2) - (satellite_vector2.ra**2 - satellite_vector1.ra**2) - (satellite_vector2.dec**2 - satellite_vector1.dec**2)
        F = (distance3**2 - distance1**2) - (satellite_vector3.ra**2 - satellite_vector1.ra**2) - (satellite_vector3.dec**2 - satellite_vector1.dec**2)

        # Check for potential division by zero
        denominator = (B * C - A * D)
        if denominator == 0:
            logging.error("Division by zero in trilateration algorithm.")
            return None

        x = (E * D - B * F) / denominator
        y = (E * C - A * F) / denominator

        # Convert Cartesian coordinates to spherical coordinates
        phi = math.atan2(math.sqrt(x**2 + y**2), 1)
        lambda_ = math.atan2(y, x)

        # Calculate the latitude and longitude of the estimated signal origin
        latitude = math.degrees(phi)
        longitude = (observer_vector1.ra - lambda_) % (2 * math.pi)
        longitude = math.degrees(longitude)

        return latitude, longitude

    except Exception as e:
        logging.error(f"Error in trilaterate_signal_origin: {e}")
        return None


def plot_satellites_and_signal_origin(satellites, signal_origin, observer):
    plt.figure(figsize=(8, 8))

    # Plot satellite locations
    for sat in satellites:
        plt.scatter(math.degrees(sat.sublong), math.degrees(sat.sublat), label=sat.name, s=100)

    # Plot observer location
    plt.scatter(math.degrees(observer.lon), math.degrees(observer.lat), label='Observer', marker='o', s=100)

    # Plot lines from observer to satellites
    for sat in satellites:
        plt.plot([math.degrees(observer.lon), math.degrees(sat.sublong)],
                 [math.degrees(observer.lat), math.degrees(sat.sublat)], linestyle='dashed', color='gray')

    # Plot line from observer to estimated signal origin
    plt.plot([math.degrees(observer.lon), signal_origin[1]],
             [math.degrees(observer.lat), signal_origin[0]], linestyle='solid', color='red', label='Trilateration')

    # Plot X marker at the estimated signal origin
    plt.scatter(signal_origin[1], signal_origin[0], marker='x', color='red', label='Signal Origin')

    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Latitude (degrees)')
    plt.title('Satellite Locations, Observer, and Signal Origin')
    plt.legend()
    plt.grid(True)
    plt.show()

