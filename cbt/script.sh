#!/bin/bash

if [ "$1" = "challenges" ]; then
#python manage.py dumpscript thought_diary.distortion thought_diary.challengequestion thought_diary.challengequestion_distortion --indent 4 > thought_diary/fixtures/challenge_and_distortion.json
python manage.py dumpdata thought_diary.distortion thought_diary.challengequestion thought_diary.challengequestion_distortion --indent 4 > thought_diary/fixtures/challenge_and_distortion.json

elif [ "$1" = "test" ]; then
python manage.py test --verbosity 2 thought_diary


elif [ "$1" = "all" ]; then
python manage.py dumpdata thought_diary.thought_distortions --indent 4 > thought_diary/fixtures/test_initial_data.json
fi
