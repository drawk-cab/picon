# picon

Display 8x8 icons on an Astro-Pi / Sense HAT based on sensor values and APIs 

## Dependencies

And how to satisfy them on a Raspberry Pi

* Python 3 (out of the box)
* `dateutil` : `sudo apt-get install python3-dateutil`
* `sense_hat` (https://pythonhosted.org/sense-hat/) : `sudo apt-get install sense-hat; sudo pip3 install pillow`

## How to run

### Display an icon

Run `./display_icon.py`

It should display a single icon until you exit the program.

By default, the icon is output to your terminal. To display
on a connected Sense HAT, run `./display_icon.py -d sense`

### Display an icon that depends on a value in a file

`./display_digit.py` looks in the file `samples/digit` for a single digit to display.

* Change the value in this file, then run `./display_digit.py`.
* Change the value while the program is running.
* What happens if you put something in the file that isn't a digit?

### Display a value in a repeating loop with a banner icon

`loop.py` can display data from any available source.

* `./loop.py digit samples/digit` will display the digit from above, but with a banner icon.
* `./loop.py random 1 10` will display random numbers from 1 to 10.

There may be more data sources installed. Run `./loop.py -h` to see them all.
You can see help for a specific data source with `./loop.py <source> -h`.

The `-l` parameter makes `loop.py` repeat the loop for a set time period:
`./loop.py -l 5` makes it run for 5 minutes.

`loop.py` also takes the `-d` parameter to display the icons on your device.

### Display several values with banner icons

The previous programs got their information from only one place: they had a single data source.
`loop.py` can use several data sources, and you can configure which ones it uses.

The supplied configuration displays the random number and the digit from `samples/digit` in turn.

### Configure different sources in a file

The data sources for `loop.py` are configured in the file `config.json`
containing the sources in the order they appear in the loop.
Each data source has parameters which apply to that source.

* The `random` source has parameters `min` and `max` which control the lowest and highest random number the source will produce.
* The `digit` source has parameter `filename` which is the file it looks in for a digit.

Try adding a second `random` source with a different range, and running `./loop.py` again.

### Display values with transitions

You can add a parameter `transition` to any data source in `config.json` to specify a transition effect:

* `wipe`
* `scroll`

### Display weather and transport information sourced from an API

(To do)

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

