#!/bin/ash
#---------- MAKE CUSTOM BINARIES AVAILABLE IN THIS SCRIPT ----------
. /home/admin/.profile

python3 /mnt/HD/HD_a2/backupandrestore/backup.py 2>&1 > /mnt/HD/HD_a2/backupandrestore/log.log
