#!/usr/bin/python

import os
import eyeD3
import mutagen, mutagen.oggvorbis

for dirpath, dirnames, filenames in os.walk('/media/music'):
   try:
      artist, album = dirpath.split('/media/music/')[1].split('/')
   except:
      continue

   media_files = [f for f in filenames if (f.endswith('ogg') or f.endswith('mp3'))]
   for mfile in media_files:
      try:
         track, title = mfile.split(' ', 1)
         track = int(track)
      except:
         continue

      path = os.path.join(dirpath, mfile)

      if mfile.endswith('mp3'):
         try:
            t = eyeD3.Tag()
            t.link(path)
            ctrack, cmax = t.getTrackNum()
         except:
            continue

         if track != ctrack:
            t.setVersion(eyeD3.tag.ID3_DEFAULT_VERSION)
            t.setTrackNum((track, len(media_files)))
            t.update()

      elif mfile.endswith('ogg'):
         try:
            t = mutagen.oggvorbis.open(path)
         except:
            continue
         else:
            try:
               ctrack = t['tracknumber'][0]
            except:
               ctrack = None

         if track != ctrack:
            t['tracknumber'] = "%02d" % track
            t.save()

      print "%s => %d on %s" % (ctrack, track, path)
