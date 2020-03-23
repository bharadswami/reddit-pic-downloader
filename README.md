# Reddit picture downloader

This Python script downloads the top images from a subreddit and automatically deletes pictures that are older than a specified number of days. Can be combined with a daemon to automatically download images every day and set them as desktop wallpaper.

## How to use
### 1. Get Client ID and Secret from Reddit
TODO

### 2. Create required_info.py
Create a file `required_info.py` and open it in your favorite text editor

Add the following information to it:
```
CLIENT_ID = <Client ID from Reddit App>
SECRET = <Secret from Reddit App>
SUBREDDIT = "<name of subreddit e.g. pics, earthporn etc."
LOG_FILE_NAME = "desired/path/to/log/file"
DEST_DIR = "path/to/where/pics/should/be/stored"
CLEANUP_DAYS = <Number of days after which the pics should be deleted"
TRASH_PATH = "path/to/Trash (usually Windows - C:\$Recycle.Bin, OSX - Users/<your username>/.Trash, Linux - ~/.local/share/Trash)"
```

### 3. Make daemon
TODO
