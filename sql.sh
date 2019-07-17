#!/usr/bin/env bash

cd accounts
python ../manage.py  makemigrations
python ../manage.py  migrate