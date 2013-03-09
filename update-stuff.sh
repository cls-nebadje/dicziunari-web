#!/bin/bash

python manage.py syncdb
python manage.py collectstatic -link --noinput
