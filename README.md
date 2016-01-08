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
* `refresh_weather.sh STATION`  will update the weather data for station number STATION (there's a script in api/ to find your station)

Add these to your crontab as you see fit.

Data is saved into the samples/ directory.

Next edit the config.json file as you want. Here you can configure
* the walk time to your station
* the display speed

Once there is data in the samples file...

`display.sh` will output icons to the terminal for testing, just once.

`sense_hat.sh N` will display them on the Sense Hat, looping for N minutes.

## To do

* Run refresh_x from python using a timer thread instead of crontab
* Plumb API config into config.json
* Provide a web interface


