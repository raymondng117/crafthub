#!/bin/bash

# Apply migrations
python manage.py migrate

# Sleep for 5 seconds after applying migrations
sleep 10

# Start Django server
python manage.py runserver 0.0.0.0:8000 &

sleep 5

# Add ngrok authentication token
ngrok authtoken 2eeA38aF68Y83aiSrWIPAvtVVSu_3Z2m73Ye9dnRzxgTQZzMr

# Expose Django server using ngrok
ngrok http --domain=terribly-content-mako.ngrok-free.app 8000