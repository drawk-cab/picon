# astropicon

Display 8x8 icons on an Astro-Pi or Unicorn-Pi based on sensor values and APIs 

## Dependencies

And how to satisfy them on a Raspberry Pi

* Python 3 (out of the box)
* `dateutil` : `sudo apt-get install python3-dateutil`
* `sense_hat` (https://pythonhosted.org/sense-hat/) : `sudo apt-get install sense-hat; sudo pip3 install pillow`

Optionally, for weather icons:

* `metoffer` for Met. Office Weather: `sudo pip3 install metoffer`
* A Met. Office API key at `~/.openldbws_api_key`

Optionally, for train icons:

* A National Rail OpenLDBWS API key at `~/.metoffice_api_key`

Also relies on the https://huxley.apphb.com/ service to convert National Rail XML into JSON

## How to run

The display program looks in the `samples` directory for API responses.

* `refresh_trains.sh ORG DST` will update the train data (ORG and DST are the 3-letter codes for origin and destination station)
* `refresh_weather.sh` will update the weather data

Add these to your crontab as you see fit.

Once there is data in `samples`...

`display.sh` will output icons to the terminal for testing, just once.

`sense_hat.sh N` will display them on the Sense Hat, looping for N minutes.

