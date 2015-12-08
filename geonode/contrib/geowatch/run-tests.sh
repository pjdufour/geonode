#!/bin/bash
export DJANGO_SETTINGS_MODULE="geonode.settings"
####################
#USER=admin
#PASS=admin
#curl -X GET -v -c cookies.txt -b cookies.txt 'http://localhost:8000'
#CSRFTOKEN=$(grep csrftoken cookies.txt | cut -f 7)
#curl -X POST -v -c cookies.txt -b cookies.txt --data "csrfmiddlewaretoken=$CSRFTOKEN&username=$USER&password=$PASS" 'http://localhost:8000/account/ajax_login'
#CSRFTOKEN=$(grep csrftoken cookies.txt | cut -f 7)
#curl -v -X POST -H "X-CSRFToken: $CSRFTOKEN" -c cookies.txt -b cookies.txt -d @test.geojson 'http://localhost:8000/geowatch/receive/geonode%3Albr_heal_pt_unmeer_ccc/geojson' > output.html
#####################
python -m unittest geonode.contrib.geowatch.tests.test_geowatch
