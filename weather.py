import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")


def print_warning(text):
	"""
	Prints a warning to `stdout` with the ANSII warning color
	:param text: The warning text to be displayed
	:return: None
	"""

	warning_color = "\033[93m"
	end_color = "\033[0m"

	print(f"{warning_color}{text}{end_color}")


def get_valid_zip():
	"""
	Gets a valid zip code through `stdin`.  Will check the zip code is valid
	with the Zippopotam API.
	:return: Zip code data (JSON/dict)
	"""

	# Continuously ask for input until a valid input is received.
	while True:

		# Ask user for zip code
		zip_code = input("Zip Code> ")

		# Ensure a zip code was provided
		if zip_code == "":
			print_warning("Enter a zip code!")
			continue

		# Check the zip code
		zip_request = requests.get(f"http://api.zippopotam.us/us/{zip_code}")
		status_code = zip_request.status_code

		# Ensure the response is valid
		if status_code == 404:
			print_warning("Invalid zip code!")
			continue
		elif status_code >= 500:
			print_warning("Server error!")
			continue

		return zip_request.json()


def parse_zip(data):
	"""
	Parse the data from a Zippopotam API request to get the city, state,
	and country of a given zip given the JSON data from a Zippopotam API
	request.
	:param data: JSON data from a Zippopotam API request (JSON/dict)
	:return: (city, state, country)
	"""

	# The closest match to the zip code entered by the user
	first_match = data["places"][0]

	# Fetch the data from the JSON data
	country = data["country abbreviation"]
	state = first_match["state abbreviation"]
	city = first_match["place name"]

	return city, state, country


def get_weather(loc, units):
	"""
	Gets the weather at a certain location.
	:param loc: The location tuple formatted as (city, state, country)
	:param units: Either "imperial" or "metric"
	:return: (current_temp, low_temp, high_temp, weather_desc)
	"""

	# Format the GET request URL
	weather_url = f"http://api.openweathermap.org/data/2.5/weather"
	weather_params = {"APPID": API_KEY, "units": units, "q": f"{loc[0]}"
															 f",{loc[1]}"
															 f",{loc[2]}"}

	# Request the weather from OpenWeatherMap
	weather_request = requests.get(weather_url, params=weather_params)

	# Ensure the response is valid
	if weather_request.status_code != 200:
		print_warning("Error fetching weather!")
		quit()

	# Parse the weather JSON data
	weather_response = weather_request.json()
	weather_desc = weather_response["weather"][0]["description"]
	current_temp = weather_response["main"]["temp"]
	min_temp = weather_response["main"]["temp_min"]
	max_temp = weather_response["main"]["temp_max"]

	return current_temp, min_temp, max_temp, weather_desc


def main():

	zip_data = get_valid_zip()
	loc = parse_zip(zip_data)
	weather = get_weather(loc, "imperial")

	print(f"The weather in {loc[0]} is {weather[3]}.  It's currently "
		  f"{weather[0]} with a low of {weather[1]} and high of {weather[2]}.")


if __name__ == "__main__":
	main()
