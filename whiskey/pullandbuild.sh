#!/bin/sh
# Lots of hard coded foo here. This is very digithink.com specific.
{   echo "====================== Start Build `date`==================="
    cd /var/www/digithink/repo
    git pull && mkdocs build 
    rm -rf ../osite
    mv ../site ../osite
    mv site ..
    cd /var/www/digithink/repo/whiskey/bartender
    mkdocs build
    cp -rpvf site/. /var/www/digithink/whiskey/bartender/
    echo "=========================== Done: `date` ===================="
}| tee logs/pullandbuild.out
