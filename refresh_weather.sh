#!/bin/bash

python3 api/metoffice.py `cat ~/.metoffice_api_key` `cat ~/.metoffice_station` > samples/metoffice

