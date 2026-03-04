#!/usr/bin/env python3
import requests
import sys

# provided in spec
API_ADDRESS = "https://www.fruityvice.com/api/fruit"

# Make a simple GET request to get the fruit
# Ensure correct arguments are being entered
if len(sys.argv) < 2:
    print("Error")
else:
    name = sys.argv[1]
    try:
        response = requests.get(f"{API_ADDRESS}/{name.lower()}", timeout=5)
    # error with making the request
    except requests.RequestException:
        print("Error")
    else:
        # fruit not found error or server error
        if response.status_code == 404 or not response.ok:
            print("Error")
        else:
            print("Found")