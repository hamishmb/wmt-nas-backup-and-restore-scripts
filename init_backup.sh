#!/bin/ash
PATH=/mnt/HD/HD_a2/nas-sysroot/usr/local/bin:/mnt/HD/HD_a2/nas-sysroot/usr/local/sbin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin

echo "test"

/mnt/HD/HD_a2/nas-sysroot/usr/local/bin/python3 /mnt/HD/HD_a2/backupandrestore/backup.py > /mnt/HD/HD_a2/backupandrestore/log.log 2> /mnt/HD/HD_a2/backupandrestore/log.log
