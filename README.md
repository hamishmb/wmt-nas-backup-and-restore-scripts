# NAS Backup and Restore Scripts

A couple of scripts to backup and restore the database. Backup is run automatically with cron.

Please note that the basic database structure needs to be present for the restore to work. If it isn't, please first use phpmyadmin to restore the structure file at: https://wmtprojectsforum.altervista.org/files/WMT%20River%20System%20Files/NAS%20Box/Setup/initial_rivercontrolsystem.sql

If the users need to be restored, download and run the SQL commands at https://wmtprojectsforum.altervista.org/files/WMT%20River%20System%20Files/NAS%20Box/Setup/user_setup_queries.txt. These can be copy and pasted all at once into the "SQL" section of the phpmyadmin interface.
