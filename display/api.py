#!/usr/bin/python3

import random
import weather
import trains
import datetime
import dateutil.parser
import json

class Api:
    '''No help for this API.'''

    @staticmethod
    def define_args(parser):
        parser.add_argument('-w', '--wait', type=float, help="Wait between frames (s)")

    def __init__(self, **args):
        self.wait = args.get("wait", 1.5)


class RandomNumber(Api):
    '''Random number'''

    @staticmethod
    def define_args(parser):
        Api.define_args(parser)
        parser.add_argument('min', type=int, help="Minimum")
        parser.add_argument('max', type=int, help="Maximum")

    def __init__(self, **args):
        Api.__init__(self, **args)
        self.min = args["min"]
        self.max = args["max"]

    def get(self):
        return (1, [weather.get_temperature( random.randrange(self.min, self.max) )], self.wait)


class MetOffice(Api):
    '''The Met. Office DataPoint API (http://www.metoffice.gov.uk/datapoint/API) via samples/metoffice'''

    @staticmethod
    def define_args(parser):
        Api.define_args(parser)
        parser.add_argument('sample', type=str, help="Sample file name")

    def __init__(self, **args):
        Api.__init__(self, **args)
        self.sample = args['sample']
        self.last_update = None
        self.value = None

    def get(self):
        with open(self.sample, 'r') as f:
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

        return (0, [type, temperature, type], self.wait)


class NationalRail(Api):
    '''The National Rail Live Departures, via Huxley / samples/nationalrail'''

    @staticmethod
    def define_args(parser):
        Api.define_args(parser)
        parser.add_argument('walk', type=int, help="Walk time, minutes")
        parser.add_argument('sample', type=str, help="Sample file name")

    def __init__(self, **args):
        Api.__init__(self, **args)
        self.last_update = None
        self.value = None
        self.walk = datetime.timedelta(0, args["walk"]*60)
        self.sample = args["sample"]

    def get(self):
        with open(self.sample, 'r') as f:
            sample = json.load(f)

            now = datetime.datetime.now()
            last_train = None
            next_train = None
            for i, data_point in enumerate(sample):
                std = dateutil.parser.parse(data_point["std"])
                etd = dateutil.parser.parse(data_point["etd"])
                if etd > (now + self.walk):
                    next_train = (etd-now, etd-std)
                    break
                last_train = (etd-now, etd-std)

            if next_train:
                wait = trains.get_time_left(next_train[0] - self.walk)

                delay_current = next_train[1].total_seconds()
                delay_trend = (next_train[1] - last_train[1]).total_seconds()

                if delay_current <= 0:
                    delay_status = trains.get_train(-1) # on time
                else:
                    # yellow if delayed less than previous train
                    # red if delayed same or more than previous train
                    delay_status = trains.get_train(delay_trend > 0)
            else:
                wait = trains.get_time_left(None)
                delay_status = trains.get_train(1)

        return (0, [delay_status, wait, delay_status], self.wait)


CHOICES = { 'random': RandomNumber,
            'metoffice': MetOffice,
            'nationalrail': NationalRail }
