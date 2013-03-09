#!/bin/bash
#
# Generate SQLite databases from anachronistic/unportable lzm files
#

cd database
./dicziunari.py -p -s
./dicziunari.py -v -s
cd ..
