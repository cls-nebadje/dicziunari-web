#!/bin/bash
sudo aptitude install python-django
sudo aptitude install python-django-registration

git submodule init
git submodule update

cd tschercha
./generate-dbs.sh
cd ..

./update-stuff.sh
