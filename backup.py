#!//usr/bin/env python3
# NAS box backup script.
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
import os
import sys
import subprocess
import datetime
import MySQLdb as mysql

#Tables to backup.
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
if not os.path.isfile("/mnt/USB/USB1/"):
    os.makedirs("/mnt/USB/USB1")
    subprocess.run(["mount", "-t", "ext4", "/dev/sdc1", "/mnt/USB/USB1"], check=False)

#If the file still isn't there then either not mounted or not the backup drive.
if not os.path.isfile("/mnt/USB/USB1/is_backupdrive"):
    sys.exit("USB not mounted or not proper backup drive")

try:
    #Connect to database w/ nasbox creds.
    database = mysql.connect(host="127.0.0.1", port=3306, user="nasbox", passwd="river20",
                             connect_timeout=30, db="rivercontrolsystem")

    cursor = database.cursor()

except:
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

backupdir = "/mnt/USB/USB1/backup-"+str(datetime.datetime.now())
os.makedirs(backupdir)

for table in tables:
    print("Backing up "+table)

    try:
        cursor.execute("SELECT * INTO OUTFILE '"+backupdir+"' from "+table+";")
        database.commit()

    except:
        print("Couldn't backup table: "+table)

    print("Done!")

print("Finished")
