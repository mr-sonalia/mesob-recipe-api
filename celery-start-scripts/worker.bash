#!/bin/bash

set -o errexit
set -o nounset

celery -A django_celery_example worker -l INFO