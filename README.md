# Python Weather Client

Simple weather client for Python 3.7.  

## Usage

The client relies on an API key from OpenWeatherMap.  See [here](https://openweathermap.org/api).  To connect with your API key, please create an environment variable as follows
```shell
$ export WEATHER_API_KEY=[api_key_here]
```
Note: your terminal will erase this environment variable after the terminal is closed unless you create a persistent variable ([see here](https://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables)).

To run the client, navigate to the directory that the `weather.py` file is located and run

```shell
$ python3 weather.py
```

