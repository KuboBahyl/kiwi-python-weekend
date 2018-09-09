#!/usr/bin/env bash

source venv/bin/activate
python src/alsa_connections.py \
    --src 'Madrid (All stops)' \
    --destination 'Barcelona (All stops)' \
    --departure '09/20/2018' \
    --passengers 1
