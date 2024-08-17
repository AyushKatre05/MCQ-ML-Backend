#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Download the spaCy model
python -m spacy download en_core_web_sm

# Start the Flask application
gunicorn app:app
