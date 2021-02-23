#!/bin/bash

set -e

cd "`dirname "$0"`"
python3.7 kox/manage.py migrate
