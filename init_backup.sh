#!/bin/ash
#---------- MAKE CUSTOM BINARIES AVAILABLE IN THIS SCRIPT ----------
. /home/admin/.profile

echo "test"

python3 /mnt/HD/HD_a2/backupandrestore/backup.py > /mnt/HD/HD_a2/backupandrestore/log.log 2> /mnt/HD/HD_a2/backupandrestore/log.log
