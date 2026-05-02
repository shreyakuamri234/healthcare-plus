#!/usr/bin/env bash
set -o errexit

# Dependencies install karein
pip install -r requirements.txt

# Static files collect karein (Healthcare+ design ke liye)
python manage.py collectstatic --no-input

# Database tables banayein
python manage.py migrate

# Admin user banayein (Aapka custom script)
python create_admin.py