#!/usr/bin/python3

import random
import weather
import trains
import datetime
import dateutil.parser
import json

class Api:
    HELP = 'No help for this API.'

    def __init__(self):
        pass

    def define_args(parser):
        pass # no arguments
    
class RandomNumber(Api):
    HELP = 'Random number'

    def __init__(self, **args):
        self.min = args["min"]
        self.max = args["max"]

    def get(self):
        return (1, [weather.get_temperature( random.randrange(self.min, self.max) )])

    def define_args(parser):
        parser.add_argument('min', type=int, help="Minimum")
        parser.add_argument('max', type=int, help="Maximum")

class MetOffice(Api):
    HELP = 'The Met. Office DataPoint API (http://www.metoffice.gov.uk/datapoint/API) via samples/metoffice'

    def __init__(self, **args):
        self.last_update = None
        self.value = None

    def get(self):
        with open('samples/metoffice', 'r') as f:
            sample = json.load(f)

            now = datetime.datetime.utcnow().isoformat()
            for data_point in sample["data"]:
                if data_point["timestamp"][0] > now:
                    break
            #print("%s: using forecast for %s" % (now, data_point["timestamp"][0]))

            try:
                temperature = data_point["Feels Like Temperature"][0]
            except:
                temperature = None

            try:
                type = data_point["Weather Type"][0]
            except:
                type = None

        temperature = weather.get_temperature(temperature)
        type = weather.get_weather_type(type)

        return (0, [type, temperature, type])


class NationalRail(Api):
    HELP = 'The National Rail Live Departures, via Huxley / samples/nationalrail'

    def __init__(self, **args):
        self.last_update = None
        self.value = None
        self.walk = datetime.timedelta(0, args["walk"]*60)

    def get(self):
        with open('samples/nationalrail', 'r') as f:
            sample = json.load(f)

            now = datetime.datetime.now()
            last_train = None
            for i, data_point in enumerate(sample):
                std = dateutil.parser.parse(data_point["std"])
                etd = dateutil.parser.parse(data_point["etd"])
                if etd > (now + self.walk):
                    next_train = (etd-now, etd-std)
                    break
                last_train = (etd-now, etd-std)

            wait = trains.get_time_left(next_train[0] - self.walk)

            delay_current = next_train[1].total_seconds()
            delay_trend = (next_train[1] - last_train[1]).total_seconds()

            if delay_current <= 0:
                delay_status = trains.get_train(-1) # on time
            else:
                # yellow if delayed less than previous train
                # red if delayed same or more than previous train
                delay_status = trains.get_train(delay_trend > 0)

        return (0, [delay_status, wait, delay_status])

    def define_args(parser):
        parser.add_argument('walk', type=int, help="Walk time, minutes")

CHOICES = { 'random': RandomNumber,
            'metoffice': MetOffice,
            'nationalrail': NationalRail }
