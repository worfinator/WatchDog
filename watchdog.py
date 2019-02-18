#!/usr/bin/python

# WatchDog
# by Mark Baldwin
#
# Python script to observe a directory for file
# changes, then upload the files to a drop box directory
# and send a notification


import ConfigParser, sys, subprocess, glob, notifier, ntpath, os.path

# Config file
config_file = '/etc/watchdog.conf'

# flags
notification_sent = False



def getConfig(config_file):
    # lets get the config
    config = ConfigParser.ConfigParser()

    # loadconfig file if it exists
    if os.path.exists(config_file):
        config.read(config_file)
        return config
    else:
        print "Error: "+ config_file + " file not found"
        sys.exit()

def uploadToDropBox(fname):
    # Upload to dropbox
    head, tail = ntpath.split(fname)
    print "Uploading "+fname+" to DropBox"
    subprocess.call(["sudo", "/usr/local/bin/dropbox_uploader.sh", "upload", fname, "/"+config.get('dropbox','upload_dir')+"/"+tail])

    # Remove file
    subprocess.call(["rm", "-f", fname])

def processFiles(filetype, notification_sent):
    # process each file
    for fname in glob.glob(config.get('watchdog','watch_dir')+"/*."+filetype):
        print "Processing " + fname
        
        # upload to dropbox if enabled
        if config.get('watchdog','dropbox_upload'):
            uploadToDropBox(fname)

        # send notification 
        if not notification_sent and config.get('watchdog','notify'):
            print "Sending Notification"
            
            message = config.get('watchdog','device_name') + " has triggered a WatchDog Alert \n"
            # add dropbox link
            if config.get('dropbox','share_link'):
                message += "\n " + config.get('dropbox','share_link')

            # Build the notification
            notifier.setConfig(config)
            notifier.setMessage(message) 
            notifier.sendNotification()
            notification_sent = True

            # create a flag file
            subprocess.call(["touch", lock_file])

    return notification_sent

# Lets get the config
config = getConfig(config_file)

# defaults
lock_file = config.get('watchdog','watch_dir') +"/lock.file"

# Only process if there is no lock file
if not os.path.exists(lock_file):

    # do an initial copy to Sync Drive
    print "Copying files to Sync Directory"
    subprocess.call(["cp","-Rvf", config.get('watchdog','watch_dir'), config.get('watchdog','remote_dir')])  

    # send email notification
    notifier.setSubject(config.get('email','subject'))

    # go through each file type
    for filetype in config.get('watchdog','file_types').split(','):
        print "Doing stuff " + filetype
    	notification_sent = processFiles(filetype, notification_sent)

    # remove the flag file
    subprocess.call(["rm", "-f", lock_file])