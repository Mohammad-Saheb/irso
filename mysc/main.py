from subprocess import call
import os


convert_result = call(["ffmpeg", "-i", "Shahram_Solati_Man(@IranSong).mp3", "-ss", "00:00:20", "-to", "00:00:40", "-ac", "1", "-map", "0:a",
                       "-codec:a", "libopus", "-b:a", "128k", "-vbr", "off", "-ar", "24000",
                       "Shahram_Solati_Man(@IranSong).ogg", "-y"], stdout=open(os.devnull, 'wb'),
                      stderr=open(os.devnull, 'wb'), stdin=open(os.devnull, 'wb'))
print(convert_result)