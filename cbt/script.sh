#!/bin/bash
python manage.py dumpdata auth.User --indent 4 > thought_diary/fixtures/test_initial_data.json