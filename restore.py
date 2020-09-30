#!/usr/bin/env python3
# NAS box restore script.
# Copyright (C) 2020 Wimborne Model Town
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 or,
# at your option, any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Version 1.0.2

import os
import sys
import subprocess
import MySQLdb as mysql

def usage():
    """
    This function is used to output help information to the standard output
    if the user passes invalid/incorrect commandline arguments.

    Usage:

    >>> usage()
    """

    print("\nUsage: restore.py [OPTION]\n\n")
    print("Options:\n")
    print("       -h, --help:                   Show this help message")
    print("       <file>                        The database archive to restore from")
    print("restore.py is released under the GNU GPL Version 3")
    print("Copyright (C) Wimborne Model Town 2020")

    sys.exit()

#Check commandline args.
if len(sys.argv) < 2:
    usage()

elif sys.argv[1] in ("-h", "--help"):
    usage()

elif not os.path.isfile(sys.argv[1]):
    sys.exit("Please specify a valid backup file")

#Tables to restore.
tables = ['SystemStatus', 'EventLog', 'SystemTick', 'NASControl', 'SUMPReadings', 'SUMPControl',
          'G3Readings', 'G3Control', 'G4Readings', 'G4Control', 'G5Readings', 'G5Control',
          'G6Readings', 'G6Control', 'VALVE1Readings', 'VALVE1Control', 'VALVE2Readings',
          'VALVE2Control', 'VALVE3Readings', 'VALVE3Control', 'VALVE4Readings',
          'VALVE4Control', 'VALVE5Readings', 'VALVE5Control', 'VALVE6Readings',
          'VALVE6Control', 'VALVE7Readings', 'VALVE7Control', 'VALVE8Readings',
          'VALVE8Control', 'VALVE9Readings', 'VALVE9Control', 'VALVE10Readings',
          'VALVE10Control', 'VALVE11Readings', 'VALVE11Control', 'VALVE12Readings',
          'VALVE12Control']

#Try to mount USB stick if not mounted.
if not os.path.isdir("/mnt/USB/USB1/"):
    os.makedirs("/mnt/USB/USB1")
    cmd = subprocess.run(["mount", "-t", "ext2", "/dev/sdc1", "/mnt/USB/USB1"],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)

    print("Mount output: "+cmd.stdout.decode("UTF-8", errors="ignore"))

#If the file still isn't there then either not mounted or not the backup drive.
if not os.path.isfile("/mnt/USB/USB1/is_backupdrive"):
    sys.exit("USB not mounted or not proper backup drive")

try:
    #Connect to database w/ backup creds.
    database = mysql.connect(host="127.0.0.1", port=3306, user="backupuser", passwd="river20",
                             connect_timeout=30, db="rivercontrolsystem")

    cursor = database.cursor()

except Exception as e:
    print("Error conecting to database: "+str(e))

    #Try to clean up gracefully.
    try:
        cursor.close()

    except Exception:
        pass

    try:
        database.close()

    except Exception:
        pass

    sys.exit("Couldn't connect to database")

backupdir = sys.argv[1].replace(".tar.gz", "")
backupname = backupdir.split("/")[-1]

print("Extracting backup")

subprocess.run(["tar", "-xvzf", backupdir+".tar.gz", "-C", "/mnt/HD/HD_a2/"], check=True)

print("Restoring tables")

for table in tables:
    print("Restoring "+table)

    try:
        cursor.execute("TRUNCATE TABLE "+table+";")
        database.commit()
        cursor.execute("LOAD DATA INFILE '/mnt/HD/HD_a2/"+backupname+"/"+table+"' INTO TABLE "+table+";")
        database.commit()

    except Exception as e:
        print("Couldn't restore table: "+table+", error was: "+str(e))

    print("Done!")

print("Finished")
