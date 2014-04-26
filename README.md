parsed
======

vk.com playlist music downloader

usage
-----
python parsed.py -u `<playlist_user>` -e `<email/phone>` -p `<password>`

After authorization with email/password script will download audio 
playlist from the user with `<playlist_user>` id.

It downloads all tracks to the `music` dir.

Script support threading and queue list of the downloading tracks.
