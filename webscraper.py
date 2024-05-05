import requests
from bs4 import BeautifulSoup
import json

# Load the JSON database
with open('airlines.json', 'r') as file:
    airlines_data = json.load(file)

# Function to scrape a particular airline's domicile information from a URL
def scrape_domiciles(url):
    """Fetch the domicile information from the provided URL.
    
    Args:
        url (str): The webpage URL to scrape.
    
    Returns:
        list: A list of dictionaries with airport code, city, and state.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data from {url}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section containing "domiciles" (case insensitive)
    domiciles_section = soup.find(text=lambda t: t and "domiciles" in t.lower())
    if not domiciles_section:
        print(f"Error: 'Domiciles' section not found in {url}")
        return []

    # Extract airport codes or data from the found section (assuming ULs and LIs)
    parent_section = domiciles_section.find_parent()  # Adjust parent selection as needed
    airport_codes = []
    for item in parent_section.find_all('li'):
        code = item.text.strip()[:3].upper()  # Extract the first three-letter code
        # Mock placeholders for city and state
        airport_codes.append({"airport_code": code, "city": "Unknown", "state": "Unknown"})

    return airport_codes

# Example usage with one airline URL (replace with actual URLs and mapping logic)
airline_url_mapping = {
    "Republic Airlines": "https://www.airlinepilotcentral.com/airlines/regional/republic_airways",  # Replace with the real URL
    "SkyWest Airlines": "https://www.airlinepilotcentral.com/airlines/regional/skywest"


}

# Update each airline's domicile data in the JSON file
for airline in airlines_data['airlines']:
    name = airline['name']
    if name in airline_url_mapping:
        print(f"Updating domiciles for {name}")
        url = airline_url_mapping[name]
        airline['pilot_domiciles'] = scrape_domiciles(url)

# Save the updated JSON data back to the file
with open('airlines.json', 'w') as file:
    json.dump(airlines_data, file, indent=4)
