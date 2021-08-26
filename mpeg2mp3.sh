# Author : q8f13
# convert mpeg files from soundcloud browser-plugin downloads
# using ffmpeg for convert from mpeg to mp3
# then move mp3 files to MusicSync folder for later sync
# then do some clean

for n in *.mpeg;
do
    ffmpeg -nostdin -i "$n" -c copy "${n%.*}.mp3"
    echo $n convert done
    sleep 1
done

mv *.mp3 ~/MusicSync/
rm *.mpeg
