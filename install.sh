#!/bin/bash
#
# * Install required packages
# * Download git submodules
# * Generate static dictionary data base
# * Run django update stuff (django data base and static files)
#

sudo aptitude install python-django
sudo aptitude install python-django-registration
sudo aptitude install python-pip
sudo pip install django-selectable

git submodule init
git submodule update

cd tschercha
./generate-dbs.sh
cd ..

./update-stuff.sh
