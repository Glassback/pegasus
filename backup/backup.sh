#!/bin/bash

THEDATE=`date +%d%m%y%H%M`

while read p; do
  tar cvf - $p/web/* | gzip -9 - > $p/backup/backup_${THEDATE}.tar
done < SitesToBackup.txt
