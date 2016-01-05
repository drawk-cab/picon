#!/bin/bash

python3 api/nationalrail.py `cat ~/.openldbws_api_key` "$1" "$2" > samples/nationalrail

