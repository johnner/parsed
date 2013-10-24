parsed
======

VK playlist music downloader

usage
-----
python parsed.py -u `<playlist_user>` -e `<email/phone>` -p `<password>`

After authorization with email/password script will download audio 
playlist of the user with `<playlist_user>` id.

It downloads all tracks to the `music` dir in the same path where script lies.

Script support threading and queue list of the downloading tracks.
