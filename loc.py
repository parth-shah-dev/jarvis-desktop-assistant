import phonenumbers
from phonenumbers import geocoder, carrier
from geopy.geocoders import Nominatim
import folium

def track_phone_number(phone_number):
    try:
        # 1. Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, None)

        # 2. Get the approximate location (country/city)
        location = geocoder.description_for_number(parsed_number, "en")
        
        # 3. Get the service provider (carrier)
        service_provider = carrier.name_for_number(parsed_number, "en")
        
        print(f"Phone Number: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f"Carrier: {service_provider}")
        print(f"General Location: {location}")

        # 4. Use a geocoding service to get latitude and longitude
        geolocator = Nominatim(user_agent="my-phone-tracker")
        loc = geolocator.geocode(location)

        if loc:
            latitude = loc.latitude
            longitude = loc.longitude
            print(f"Latitude: {latitude}, Longitude: {longitude}")

            # 5. Create a map and save it
            my_map = folium.Map(location=[latitude, longitude], zoom_start=9)
            folium.Marker([latitude, longitude], popup=location).add_to(my_map)
            
            map_filename = f"map_{parsed_number.national_number}.html"
            my_map.save(map_filename)
            print(f"Map saved to {map_filename}")

        else:
            print("Could not find a specific location. Only general location is available.")

    except Exception as e:
        print(f"An error occurred: {e}. Please ensure the phone number is in the correct format (e.g., +91... or +1...).")

# Example usage: Replace with the phone number you want to track
# Make sure to include the country code
phone_number_to_track = "+917990125633" 
track_phone_number(phone_number_to_track)