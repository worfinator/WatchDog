# WatchDog
Python script to observe a directory for file changes, then upload the files to a drop box directory and send a notification

## Requirements

WatchDog uses the Python [Notifier](https://github.com/worfinator/Notifier) module to be already installed in the `/usr/local/bin/` directory in order to send emails and push notifications

## Installation 

Download and unpack [watchdog.py](watchdog.py) to the `/usr/local/bin` directory. 

```bash
cp watchdog.py /usr/local/bin
chmod 755 /usr/local/bin/watchdog.py
```

Copy [dropbox_uploader.sh](dropbox_uploader.sh) to `/usr/local/bin` directory.
```bash
cp dropbox_uploader.sh /usr/local/bin
chmod 755 /usr/local/bin/dropbox_uploader.sh
```

Copy [etc/watchdog.conf](etc/watchdog.conf) to the `/etc/` directory.
```bash
cp watchdog.conf /etc/watchdog.conf
```

## Configuration

Edit the [/etc/watchdog.conf](etc/watchdog.conf) file and change the settings to suit your own WatchDog process.

`remote_dir` - Dropbox remote directory (This is usually a mounted drive path).

`file_types` - file extensions you wish to track for changes.

`watch_dir` - directory you wish to track file changes in.

`dropbox_upload` (on/off) - toggle dropbox upload

`notify` (on/off) - toggle notifications

You will also need to configure your own values for the DropBox, Notfitier, Email and Notification services.


## Execution

Add the watchdog.py script as a CRON job that runs every 1 minute using the following format

`1 * * * * /usr/local/bin/watchdog.py`

