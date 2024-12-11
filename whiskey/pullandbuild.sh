#!/bin/sh
cd /var/www/digithink
git pull && mkdocs build -d stage
cp -r overrides stage/
rm -rf osite
mv site osite
mv stage site
cd /var/www/digithink/whiskey/bartender
git pull && mkdocs build
cp -rpvf site/. .
