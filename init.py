#!/usr/bin/env python

from glob import glob
from pydub import AudioSegment
from pydub.generators import WhiteNoise
from math import *
from random import *
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-i', type=str,
                    metavar='Source audio path', required=True,
                    help='Path to source file.')
parser.add_argument('-o', type=str,
                    metavar='Modified audio path', required=True,
                    help='Path to modified file.')

args = parser.parse_args()

if not args.i and not i:
    raise Exception('Missing -i Input option')
if not args.o and not o:
    raise Exception('Missing -o Output option')

# if len(sys.argv) > 2:
# 	AudioSegment.converter = sys.argv[1] #ffmpeg installation exe dir path
# 	AudioSegment.ffmpeg = sys.argv[1] #ffmpeg installation exe dir path
# 	AudioSegment.ffprobe = sys.argv[2] #ffprobe installation exe dir path

def calc_pan(index):
	return cos(radians(index))

#playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("mp3/*.mp3")]

#first_song = playlist_songs.pop(0)
interval = 0.2 * 1000 # sec
song = AudioSegment.from_mp3(args.i)
song_inverted = song.invert_phase()
song.overlay(song_inverted)

splitted_song = splitted_song_inverted = []
song_start_point = 0

print("Splitting track " + args.i + " in parts......")
while song_start_point+interval < len(song):
    splitted_song.append(song[song_start_point:song_start_point+interval])
    song_start_point += interval

if song_start_point < len(song):
    splitted_song.append(song[song_start_point:])

print("End of splitting......")
print("total pieces: " + str(len(splitted_song)))

ambisonics_song = splitted_song.pop(0)
pan_index = 0
for piece in splitted_song:
    pan_index += 5
    piece = piece.pan(calc_pan(pan_index))
    ambisonics_song = ambisonics_song.append(piece, crossfade=interval/50)

# lets save it!
out_f = open("8d.mp3", 'wb')

ambisonics_song.export(out_f, format='mp3')

subprocess.call("ffmpeg -i 8d.mp3 -codec:a libmp3lame -b:a 320k " + args.o, shell=True)
