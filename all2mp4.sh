for i in videos/*.webm; do ffmpeg -i "$i" "${i%.*}.mp4"; rm $i;done
for i in videos/*.mkv; do ffmpeg -i "$i" "${i%.*}.mp4"; rm  $i;done