
# Satellite Signal Trilateration

## Overview

This project demonstrates the trilateration of a signal's origin using the distances from three satellites. It utilizes the ephem Python library for high-precision astronomy computations and includes modules for fetching satellite information from the Celestrak website, performing trilateration, and visualizing the results.

## Files

### `satellite_data.py`

This module provides functions to fetch satellite information from the Celestrak website, including a list of satellites and their Two-Line Element (TLE) data.

Note: Celestrak data may change, and it's recommended to check their website for the most up-to-date information.

### `ephem_trilateration.py`

This module contains functions for signal trilateration using satellite distances. (See the algorithm below) It includes the trilateration algorithm and functions for plotting satellite locations, the observer's location, and the estimated signal origin.

### `main.py`

This script demonstrates signal trilateration using satellite distances. It fetches a list of satellites from the Celestrak website, allows the user to select three satellites, retrieves their TLE data, and performs trilateration to estimate the signal origin.

You can set the observer location in this file.  By default, the lat, lon is set to Huntsville, AL.

### `ephemeris_cache.txt`

This file is used to CACHE the last ephemeris data pulled from Celestrak. This aids in a useful function where I ensure that I always have
data even if I have no internet connection.

## Running the Project

1. Install dependencies:

   ```bash
   pip install ephem requests matplotlib
   pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04 wxPython
   sudo apt-get install git curl libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0
   ```

   Replace sudo apt-get with `brew` if you're on MacOS.

2. Run the `main.py` script:

   ```bash
   python main.py
   ```

Follow the on-screen instructions to select three satellites and observe the estimated signal origin.

I'm currently working on getting this all in a pipenv environment. So, some of this might change. I am not able to use the plot animation function that I have chosen in a pipenv (virtual environment).  The Pipfile is included, but I have not included instructions for running inside of a virtual environment knowing that functionality is not available.

## Trilateration Algorithm

The trilateration algorithm employed in this project relies on mathematical equations and spherical coordinate transformations to estimate the latitude and longitude of a signal origin based on the distances from an observer to three satellites. The key formulas involved are as follows:

### Formulas

1. **Coordinate Transformation:**
   - Convert Cartesian coordinates `(x, y)` to spherical coordinates `(φ, λ)`:

     \[ \phi = \text{atan2}\left(\sqrt{x^2 + y^2}, 1\right) \]
     \[ \lambda = \text{atan2}(y, x) \]

   where \(\phi\) is the latitude, \(\lambda\) is the longitude, and \(\text{atan2}\) is the arctangent function.

2. **Trilateration:**
   The trilateration algorithm used in this project involves solving a system of equations derived from the distances between the observer and three satellites (3 known points) similar to how GPS calculates the position.

    \[ A = 2 \cdot (\text{{satellite\_vector2.ra}} - \text{{satellite\_vector1.ra}}) \]

    \[ B = 2 \cdot (\text{{satellite\_vector2.dec}} - \text{{satellite\_vector1.dec}}) \]

    \[ C = 2 \cdot (\text{{satellite\_vector3.ra}} - \text{{satellite\_vector1.ra}}) \]

    \[ D = 2 \cdot (\text{{satellite\_vector3.dec}} - \text{{satellite\_vector1.dec}}) \]

    \[ E = (d_2^2 - d_1^2) - (\text{{satellite\_vector2.ra}}^2 - \text{{satellite\_vector1.ra}}^2) - (\text{{satellite\_vector2.dec}}^2 - \text{{satellite\_vector1.dec}}^2) \]

    \[ F = (d_3^2 - d_1^2) - (\text{{satellite\_vector3.ra}}^2 - \text{{satellite\_vector1.ra}}^2) - (\text{{satellite\_vector3.dec}}^2 - \text{{satellite\_vector1.dec}}^2) \]

    \[ x = \frac{{E \cdot D - B \cdot F}}{{B \cdot C - A \cdot D}} \]

    \[ y = \frac{{E \cdot C - A \cdot F}}{{A \cdot D - B \cdot C}} \]

   where \(d_1, d_2, d_3\) are the distances from the observer to the signal source via each satellite and \(ra, dec\) stand for right ascension and declination, respectively.

These formulas form the core of the trilateration process, allowing the derivation of the signal origin's geographical coordinates.
