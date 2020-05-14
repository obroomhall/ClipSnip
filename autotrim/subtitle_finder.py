from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import tmdbsimple as tmdb
import os
import srt
from ffsubsync import subsync
import media_filename_parser


class SubtitleFinder:



    def __init__(self, dir_name, ost_username, ost_password, tmdb_key):
        self.ost = OpenSubtitles()
        self.login(ost_username, ost_password)
        self.ost_language = 'eng'
        self.dir_name = dir_name
        tmdb.API_KEY = tmdb_key
        self.tmdb_language = 'en'
        self.subsync_parser = subsync.make_parser()

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

        subtitles = read_subtitles(subs_filename)

        # subsync doesn't like some srt files from OpenSubtitles, so we
        # save them to our own file with utf-8 encoding
        encoded_subs_filename = os.path.join(self.dir_name, 'encoded.srt')
        with open(encoded_subs_filename, 'w') as f:
            f.write(srt.compose(subtitles))

        synced_subs_filename = os.path.join(self.dir_name, 'synced.srt')
        self.run_subsync(video_filename, encoded_subs_filename, synced_subs_filename)
        return synced_subs_filename

    def run_subsync(self, reference, srtin, srtout):
        subsync_args = self.subsync_parser.parse_args([
            reference,
            '-i', srtin,
            '-o', srtout
        ])
        subsync.run(subsync_args)


def read_subtitles(filename):
    with open(filename, 'r') as f:
        raw_subs = f.read()
        subtitle_generator = srt.parse(raw_subs)
        return list(subtitle_generator)


def find_imdb_id(filename):

    search = tmdb.Search()
    parsed = media_filename_parser.parse(filename)

    if parsed.is_movie():
        if parsed.year:
            response = search.movie(
                query=parsed.title,
                year=parsed.year)
            if 'results' not in response or ('results' in response and not response['results']):
                response = search.movie(query=parsed.title)
        else:
            response = search.movie(query=parsed.title)

        movie = tmdb.movies.Movies(response['results'][0]['id'])
        return movie.external_ids()['imdb_id']

    else:
        response = search.tv(query=parsed.title)
        tmdb_id = response['results'][0]['id']
        tv = tmdb.tv.TV_Episodes(tmdb_id, parsed.season, parsed.episode)
        return tv.external_ids()['imdb_id']
