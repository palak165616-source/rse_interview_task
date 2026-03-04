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
    
    # try except block for errors regarding the JSON response
    try:
        return response.json()
    except ValueError:
        raise API_Request_Error("Failed to parse JSON response.")
    
"""
function for printing the JSON response in a human-readable format
"""
def human_readable(fruit: dict) -> str:
    nutr = fruit.get("nutritions", {})

    # return required information
    return (
        f"Fruit: {fruit.get('name')}\n"
        f"ID: {fruit.get('id')}\n"
        f"Family: {fruit.get('family')}\n"
        f"Sugar (g): {nutr.get('sugar')}\n"
        f"Carbohydrates (g): {nutr.get('carbohydrates')}"
    )

def main():

    # Ensure correct arguments are being entered
    if len(sys.argv) < 2:
        print("Usage: py fruit.py <fruit>")
        return

    name = sys.argv[1]
    try:
        fruit_data = fetch_fruit(name)
    except API_Request_Error as e:
        print(f"Error: {e}")
    else:
        print(human_readable(fruit_data))

if __name__ == "__main__":
    sys.exit(main())
