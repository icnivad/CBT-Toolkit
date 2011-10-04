#!/bin/bash

if [ "$1" = "challenges" ]; then
#python manage.py dumpscript thought_diary.distortion thought_diary.challengequestion thought_diary.challengequestion_distortion --indent 4 > thought_diary/fixtures/challenge_and_distortion.json
python manage.py dumpdata thought_diary.distortion thought_diary.challengequestion --indent 4 > thought_diary/fixtures/challenge_and_distortion.json

elif [ "$1" = "test" ]; then
python manage.py test --verbosity 2 thought_diary

elif [ "$1" = "dump" ]; then
python manage.py dumpdata sites.site --indent 4 > main/fixtures/site_data.json


elif [ "$1" = "load" ]; then
python manage.py loaddata main/fixtures/site_data.json

elif [ "$1" = "load_thought" ]; then
python manage.py loaddata thought_diary/fixtures/original_data.json

elif [ "$1" = "load_distortions" ]; then
python manage.py loaddata thought_diary/fixtures/original_challenge_and_distortion.json

elif [ "$1" = "all" ]; then
python manage.py dumpdata thought_diary --indent 4 > thought_diary/fixtures/original_data.json
fi
