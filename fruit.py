#!/usr/bin/env python3
"""
Fruit lookup utility using the Fruityvice API.

This module provides:
  - A tool to fetch information about fruits
  - Functions for human-readable and machine-readable output

Usage:
    py fruit.py <fruitname> [--machine]

Dependencies:
    requests

Functions:
    fetch_fruit(name): Query the Fruityvice API for the given fruit.
    human_readable(fruit): Format the fruit data for humans.
    machine_readable(fruit): Format the fruit data as JSON.
"""

import requests
import sys
import argparse
import json

# provided in spec
API_ADDRESS = "https://www.fruityvice.com/api/fruit"


class API_Request_Error(Exception):
    """
    Exception raised when a request to the Fruityvice API fails.

    This can occur due to network issues, server errors,
    missing fruit names, or invalid JSON responses.
    """
    pass

# making the GET request a separate function helps make it work as a library function
def fetch_fruit(name):

    """
    Fetch fruit details from the Fruityvice API.

    Parameters-
    name : str
        The name of the fruit to query.

    Returns-
    dict
        Parsed JSON of fruit data.

    Raises-
    API_Request_Error
        If the network request fails, the fruit is not found, or the
        response cannot be parsed as JSON.
    """

    # Make a simple GET request to get the fruit
    try:
        response = requests.get(f"{API_ADDRESS}/{name.lower()}", timeout=5)
    # error with making the request
    except requests.RequestException as exc:
        raise API_Request_Error(f"API request failed: {exc}")

    # fruit not found error
    if response.status_code == 404:
        raise API_Request_Error(f"Fruit '{name}' not found in database.")
    
    # server error
    if not response.ok: 
        raise API_Request_Error(f"Error from server: {response.status_code}")
    
    # try except block for errors regarding the JSON response
    try:
        return response.json()
    except ValueError:
        raise API_Request_Error("Failed to parse JSON response.")
    

def human_readable(fruit: dict) -> str:
    """
    Format fruit data into a human-readable string.

    Parameters-
    fruit : dict
        The JSON object returned from the Fruityvice API for a given fruit.

    Returns-
    str
        A multi-line string containing:
          - Fruit name
          - ID
          - Family
          - Sugar content
          - Carbohydrate content
    """
    nutr = fruit.get("nutritions", {})

    # return required information
    return (
        f"Fruit: {fruit.get('name')}\n"
        f"ID: {fruit.get('id')}\n"
        f"Family: {fruit.get('family')}\n"
        f"Sugar (g): {nutr.get('sugar')}\n"
        f"Carbohydrates (g): {nutr.get('carbohydrates')}"
    )


def machine_readable(fruit: dict) -> str:
    """
    Format fruit data into machine-readable JSON.

    Parameters-
    fruit : dict
        The JSON object returned from the Fruityvice API for a given fruit.

    Returns-
    str
        A JSON string with selected fields:
          - name
          - id
          - family
          - nutritions.sugar_g
          - nutritions.carbohydrates_g
    """

    # return required information
    output = {
        "name": fruit.get("name"),
        "id": fruit.get("id"),
        "family": fruit.get("family"),
        "nutritions": {
            "sugar_g": fruit.get("nutritions", {}).get("sugar"),
            "carbohydrates_g": fruit.get("nutritions", {}).get("carbohydrates")
        }
    }
    return json.dumps(output, indent=2)

def main():

    # Ensure correct arguments are being entered
    # tags to print information in a machine readle format
    parser = argparse.ArgumentParser(description="Lookup fruit details from Fruityvice API.")
    parser.add_argument("fruit", help="fruit to lookup")
    parser.add_argument(
        "-m", "--machine",
        action="store_true",
        help="Output fruit details in machine-readable JSON"
    )

    args = parser.parse_args()

    try:
        fruit_data = fetch_fruit(args.fruit)

    # print respective error message
    except API_Request_Error as e:
        print(f"Error: {e}")
        return 1

    # print in a machine readable JSON format
    if args.machine:
        print(machine_readable(fruit_data))

    # print in a human readable format
    else:
        print(human_readable(fruit_data))

    return 0

if __name__ == "__main__":
    sys.exit(main())
