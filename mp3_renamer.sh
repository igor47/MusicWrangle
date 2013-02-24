#!/bin/bash
TITLE="`id3tool "$1" | grep '^Song Title:' | awk '{ for (i=3;i<=NF;i++) { printf $i; printf " " } }'`"
ARTIST="`id3tool "$1" | grep '^Artist:' | awk '{ for (i=2;i<=NF;i++) { printf $i; printf " " } }'`"
ALBUM="`id3tool "$1" | grep '^Album:' | awk '{ for (i=2;i<=NF;i++) { printf $i; printf " " } }'`"
YEAR="`id3tool "$1" | grep '^Year:' | awk '{ for (i=2;i<=NF;i++) { printf $i; printf " " } }'`"
TRACKNUM="`id3tool "$1" | grep '^Track:' | awk '{ print $2 }'`"

mv "$1" "$TRACKNUM $1"

