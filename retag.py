#!/usr/bin/python

import os
import eyeD3

for dirpath, dirnames, filenames in os.walk('/media/music'):
   try:
      artist, album = dirpath.split('/media/music/')[1].split('/')
   except:
      continue

   mp3s = filter(lambda f: f.endswith('mp3'), filenames)
   for mp3 in mp3s:
      try:
         track, title = mp3.split(' ', 1)
         track = int(track)
      except:
         continue

      path = os.path.join(dirpath, mp3)

      try:
         t = eyeD3.Tag()
         t.link(path)
         ctrack, cmax = t.getTrackNum()
      except:
         continue

      if track != ctrack:
         t.setVersion(eyeD3.tag.ID3_DEFAULT_VERSION)
         t.setTrackNum((track, len(mp3s)))
         t.update()
         print "%s => %d on %s" % (ctrack, t.getTrackNum()[0], path)
