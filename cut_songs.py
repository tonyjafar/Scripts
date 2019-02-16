from pydub import AudioSegment
import argparse
import os


def getargs():
    parser = argparse.ArgumentParser(description='Edit songs')

    parser.add_argument('-fl', '--between', required=False, action='store', nargs='+', type=int,
                        help='first and last portion separate by a space in seconds.')
    parser.add_argument('-f', '--first', required=False, action='store',
                        help='first portion in seconds', type=int)
    parser.add_argument('-l', '--last', required=False, action='store',
                        help='last portion in seconds', type=int)
    parser.add_argument('-s', '--song', required=True, action='store', help='song to edit path.')

    parser.add_argument('-d', '--directory', required=True, action='store')

    args = parser.parse_args()
    return args


my_args = getargs()

song = AudioSegment.from_mp3(my_args.song)

if not my_args.between and not my_args.first and not my_args.last:
    print('one of fl/f/l should be given in args')
    exit(2)


if my_args.first:
    my_portion = my_args.first * 1000
    only_song = song[my_portion:]

elif my_args.last:
    my_portion = my_args.last * 1000
    only_song = song[:my_portion]

elif my_args.between:
    my_begin = my_args.between[0] * 1000
    my_end = my_args.between[1] * 1000
    only_song = song[my_begin:my_end]
try:
    os.chdir(my_args.directory)
    only_song.export("edited.mp3", format="mp3")
except Exception as e:
    print(e)
    exit(2)
