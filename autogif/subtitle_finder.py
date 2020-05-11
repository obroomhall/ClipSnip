from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import PTN
import tmdbsimple as tmdb
import os
import subprocess
import srt


class SubtitleFinder:

    def __init__(self, dir_name):
        self.ost = OpenSubtitles()
        self.login(os.environ['ost_username'], os.environ['ost_password'])
        self.ost_language = 'eng'
        self.dir_name = dir_name
        tmdb.API_KEY = os.environ['tmdb_key']
        self.tmdb_language = 'en'

    def login(self, username, password):
        self.ost.login(username, password)

    def download_subtitles(self, source, imdb_id=None):

        if imdb_id:
            data = self.ost.search_subtitles([{
                'sublanguageid': self.ost_language,
                'imdbid': imdb_id if imdb_id[:2] != 'tt' else imdb_id[2:],
            }])
            synced = False
        else:
            f = File(source)
            data = self.ost.search_subtitles([{
                'sublanguageid': self.ost_language,
                'moviehash': f.get_hash(),
                'moviebytesize': f.size
            }])

            if data:
                synced = True
            else:
                filename = source.split('/')[-1]
                try:
                    imdb_id = find_imdb_id(filename)
                except Exception:
                    raise Exception("Failed to find media in IMDb. Try specifying an IMDb ID with -i or --imdb-id.")
                data = self.ost.search_subtitles([{
                    'sublanguageid': self.ost_language,
                    'imdbid': imdb_id if imdb_id[:2] != 'tt' else imdb_id[2:],
                }])
                synced = False

        try:
            id_subtitle_file = data[0].get('IDSubtitleFile')
        except Exception:
            raise Exception("Failed to find media in IMDb for ID={0}.".format(imdb_id))

        self.ost.download_subtitles([id_subtitle_file], output_directory=self.dir_name)
        subtitle_filename = os.path.join(self.dir_name, id_subtitle_file + '.srt')

        return [subtitle_filename, synced]

    def sync_subtitles(self, video_filename, subs_filename):

        subtitles = self.read_subtitles(subs_filename)

        # subsync doesn't like some srt files from OpenSubtitles, so we
        # save them to our own file with utf-8 encoding
        encoded_subs_filename = os.path.join(self.dir_name, 'encoded.srt')
        with open(encoded_subs_filename, 'w') as f:
            f.write(srt.compose(subtitles))

        # runs subsync via command line because their python library is undocumented
        synced_subs_filename = os.path.join(self.dir_name, 'synced.srt')
        subprocess.run([
            'subsync',
            video_filename,
            '-i', encoded_subs_filename,
            '-o', synced_subs_filename
        ], check=True)

        return synced_subs_filename

    def read_subtitles(self, filename):
        with open(filename, 'r') as f:
            raw_subs = f.read()
            subtitle_generator = srt.parse(raw_subs)
            return list(subtitle_generator)


def find_imdb_id(filename):

    name_info = PTN.parse(filename)
    search = tmdb.Search()

    if 'season' in name_info and 'episode' in name_info:
        response = search.tv(query=name_info['title'])
        tmdb_id = response['results'][0]['id']
        tv = tmdb.tv.TV_Episodes(tmdb_id, name_info['season'], name_info['episode'])
        return tv.external_ids()['imdb_id'][2:]
    else:
        if 'year' in name_info:
            response = search.movie(
                query=name_info['title'],
                year=name_info['year'])
            if 'results' not in response or ('results' in response and not response['results']):
                response = search.movie(query=name_info['title'])
        else:
            response = search.movie(query=name_info['title'])

        movie = tmdb.movies.Movies(response['results'][0]['id'])
        return movie.external_ids()['imdb_id'][2:]
