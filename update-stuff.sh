#!/bin/bash
#
# Update django data base
# Update static files (non-interactivly)
#

python manage.py syncdb
python manage.py collectstatic -link --noinput
