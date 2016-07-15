#!/usr/bin/python

import os, os.path
import mutagen

# root music directory. this is where all music is stored. we assume
# that every directory under this root corresponds to an artist name
root_music_dir = '/media/music'

# these are the fields we'd like to set on tracks
fields = ['album', 'artist', 'title', 'tracknumber']

def walk_media(root):
   for dirpath, dirnames, filenames in os.walk(root):
      dir_without_root = dirpath.split(root_music_dir)[1]
      parts = dir_without_root.split('/')[1:]
      if len(parts) == 1:
         artist = parts[0]
         album = None
      elif len(parts) == 2:
         artist = parts[0]
         album = parts[1]
      else:
         continue

      for name in filenames:
         # derive track and title
         without_extension = os.path.splitext(name)[0]
         try:
            track, title = without_extension.split(' ', 1)
         except:
            title = without_extension
            track = None

         # make sure track is an integer (even though we keep it as a string)
         if track is not None:
            try:
               int(track)
            except:
               title = without_extension
               track = None

         # is this a media file? find out by creating a mutagen FileType object
         path = os.path.join(dirpath, name)
         try:
            ft = mutagen.File(path, easy = True)
         except Exception, e:
            print "%-30s: invalid file, i guess? %s" % (path, e)
            continue

         # this was not a media file that mutagen recognized 
         if ft is None:
            print "%-30s: skipped (notmedia)" % path
            continue

         if type(ft) == mutagen.aiff.AIFF:
            print "%-30s: skipped (aiff unsupported)" % path
            continue

         if type(ft) == mutagen.aac.AAC:
            print "%-30s: skipped (aac unsupported)" % path
            continue

         # if we don't have any tags, lets add some
         if ft.tags is None:
            ft.add_tags()

         # now lets set the fields that are missing
         computed_fields = {
               'artist': artist,
               'album': album,
               'title': title,
               'tracknumber': track,
               }

         updated_fields = {}
         disagreed_fields = {}

         for field, value in computed_fields.items():
            # skip if we don't even know what the right value should be
            if value is None:
               continue

            # is the value already set? if so we don't update it, but we do log disagreements
            try:
               existing_value = ft.tags[field]

               # sometimes, it's a list
               try:
                  existing_value = existing_value[0]
               except IndexError:
                  pass

               if field == 'tracknumber':
                  try:
                     existing_value = int(existing_value)
                  except ValueError:
                     try:
                        existing_value = int(existing_value.split('/')[0])
                     except ValueError:
                        pass

                  if existing_value != int(value):
                     disagreed_fields[field] = (existing_value, value)
               else:
                  possible_values = [existing_value]
                  try:
                     possible_values.append(existing_value.lower())
                  except AttributeError:
                     pass

                  if value not in possible_values:
                     disagreed_fields[field] = (existing_value, value)

         # we definitely want to save if we have updated fields
         if len(updated_fields) > 0:
            print "%-30s: updated: %s" % (path, updated_fields)

            try:
               ft.save(v1=mutagen.id3.ID3v1SaveOptions.REMOVE)
            except TypeError:
               ft.save()

         # if we do not have updated fields, we may still want to delete v1 tags
         else:
            mutagen.id3.ID3().delete(ft.filename, delete_v1 = True, delete_v2 = False)

         if len(disagreed_fields) > 0:
            print "%-30s: disagreed: %s" % (path, disagreed_fields)

if __name__ == "__main__":
   walk_media('/media/music')
