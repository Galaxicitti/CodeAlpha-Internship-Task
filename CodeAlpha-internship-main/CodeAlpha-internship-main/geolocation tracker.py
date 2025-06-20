import requests
from geopy.geocoders import Nominatim
import folium

def get_ip_location():
    # this is to get the public ip adress
    ip_address = requests.get('https://api64.ipify.org?format=json').json()['ip']
    
    # Get geolocation information
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    
    if 'error' not in response:
        return {
            'ip': ip_address,
            'city': response.get('city'),
            'region': response.get('region'),
            'country': response.get('country_name'),
            'latitude': response.get('latitude'),
            'longitude': response.get('longitude')
        }
    else:
        return None

def create_map(latitude, longitude, city):
    # this is to create a map using the user location
    user_map = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Add a marker
    folium.Marker([latitude, longitude], tooltip=city).add_to(user_map)
    
    # Save the map to a HTML file which can be run to find the map with the marker
    user_map.save("user_location_map.html")

if __name__ == "__main__":
    location_data = get_ip_location()
    
    if location_data:
        print(f"IP Address: {location_data['ip']}")
        print(f"Location: {location_data['city']}, {location_data['region']}, {location_data['country']}")
        print(f"Coordinates: ({location_data['latitude']}, {location_data['longitude']})")
        
        create_map(location_data['latitude'], location_data['longitude'], location_data['city'])
        print("Map has been saved as 'user_location_map.html'")
    else:
        print("Could not retrieve location data.")
