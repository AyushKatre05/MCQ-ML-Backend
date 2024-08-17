#!/bin/sh
# Install SpaCy model
python -m spacy download en_core_web_sm

# Run Gunicorn
gunicorn backend.app:app --bind 0.0.0.0:8000 --chdir backend
