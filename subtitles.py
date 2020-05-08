import os
from pythonopensubtitles.opensubtitles import OpenSubtitles
import srt

ost_username = os.environ['ost_username']
ost_password = os.environ['ost_password']

ost = OpenSubtitles()
#ost.login(ost_username, ost_password)


def download_subtitles(imdb_id):

    data = ost.search_subtitles([{
        'sublanguageid': 'eng',
        'imdbid': imdb_id,
    }])
    id_subtitle_file = data[0].get('IDSubtitleFile')

    ost.download_subtitles([id_subtitle_file], output_directory='D:/Videos/Media/', extension='srt')


def parse_subtitles(filename):
    f = open(filename, "r")
    subtitle_generator = srt.parse(f.read())
    subtitles = list(subtitle_generator)

    print(subtitles[0].start)
    print(subtitles[4].content)
