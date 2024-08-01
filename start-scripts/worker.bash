#!/bin/bash

set -o errexit
set -o nounset

celery -A config.celery worker -c 4 -l INFO
