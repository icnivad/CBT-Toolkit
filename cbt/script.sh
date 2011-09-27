#!/bin/bash
python manage.py dumpdata thought_diary --indent 4 > thought_diary/fixtures/test_initial_data.json
