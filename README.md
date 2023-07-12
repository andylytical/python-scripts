# General Usage
1. Deploy a container with this repo: `bash go.sh`
1. Run a python script: `python <SCRIPTNAME.py>`

## Audio file extended tags
* Start the container (per #1 above)
* `mount -t cifs //192.168.50.31/Music /media
   -o iocharset=utf8
   -o user=USERNAME,password="password"`
* `python xtended_tags.py -h`
* `time python xtended_tags.py -P -t TAGNAME /media/Shared >/home/Downloads/playlist.m3u8`
