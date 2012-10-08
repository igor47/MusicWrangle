MusicWrangle
============

This repo is a collection of scripts for managing the Moomers media archive.
All of the scripts here expect the canonical filenaming of moomers music.
The structure is:
     music
       |
       - artist1
       -- sometrack.ogg
       |
       - artist2
       |
       -- random_track.ogg
       -- album
        |
        -- 01 trackname.ogg
        -- 02 anothertrack.ogg
        -- 03 yetmore.ogg
        -- cover.jpg


retag.py
-------

This is a little python program that walks down the music archive and re-tags files based on filename.
