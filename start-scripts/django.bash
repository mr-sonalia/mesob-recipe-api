#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

gunicorn config.wsgi:application --bind 0.0.0.0:8000 