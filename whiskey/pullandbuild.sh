#!/bin/sh
cd /var/www/digithink
git pull && mkdocs build -d stage
rm -rf osite
mv site osite
mv stage site
