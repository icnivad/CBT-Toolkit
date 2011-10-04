#!/bin/bash

#backup production database
mysqldump -utukipenda_cbt_p -pther@1npounds tukipenda_cbt_p | gzip > ~/bkups/cbt_production/database_cbt_prod_$(date +%m-%d-%Y).sql 2>> ~/bkups/cron.log