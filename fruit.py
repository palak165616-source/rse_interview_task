#!/usr/bin/env python3
import requests
import sys

# provided in spec
API_ADDRESS = "https://www.fruityvice.com/api/fruit"

"""
custom exception/error handler for API request failure
"""
class API_Request_Error(Exception):
    pass

# making the GET request a separate function helps make it work as a library function
def fetch_fruit(name):

    # Make a simple GET request to get the fruit
    try:
        response = requests.get(f"{API_ADDRESS}/{name.lower()}", timeout=5)
    # error with making the request
    except requests.RequestException:
        raise API_Request_Error(f"API request failed: {exc}")

    # fruit not found error
    if response.status_code == 404:
        raise API_Request_Error(f"Fruit '{name}' not found in database.")
    
    # server error
    if not response.ok: 
        raise API_Request_Error(f"Error from server: {response.status_code}")
    
    else:
        print("Found")

def main():

    # Ensure correct arguments are being entered
    if len(sys.argv) < 2:
        print("Error: No fruit given")
        return

    name = sys.argv[1]
    try:
        fetch_fruit(name)
    except API_Request_Error:
        print("Error")

if __name__ == "__main__":
    sys.exit(main())
