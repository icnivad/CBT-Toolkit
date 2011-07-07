#!/bin/bash
python manage.py dumpdata thought_diary --all thought_diary --indent 4 > thought_diary/Fixtures/thought.json