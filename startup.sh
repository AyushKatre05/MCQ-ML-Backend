#!/bin/sh
# Start Gunicorn
gunicorn app:app --bind 0.0.0.0:8000
