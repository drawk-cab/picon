#!/bin/bash

export HUXLEY_ACCESS_TOKEN=$(cat ~/.huxley_access_token)
export HUXLEY_START_CRS="FOG"
export HUXLEY_END_CRS="LST"
export HUXLEY_SERVICE="train"

python3 ./huxley_uk_trains.py

