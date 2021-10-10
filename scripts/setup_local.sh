#!/bin/sh

virtualenv -p `which python3.8` env
source env/bin/activate
pip install -r requirements.txt

