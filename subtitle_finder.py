import os
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import PTN
import tmdbsimple as tmdb


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

    def download_subtitles(self, source):

        f = File(source)
        data = self.ost.search_subtitles([{
            'sublanguageid': self.ost_language,
            'moviehash': f.get_hash(),
            'moviebytesize': f.size
        }])

        if data:
            id_subtitle_file = data[0].get('IDSubtitleFile')
        else:
            filename = source.split('/')[-1]
            imdb_id = self.find_imdb_id(filename)
            data = self.ost.search_subtitles([{
                'sublanguageid': self.ost_language,
                'imdbid': imdb_id,
            }])
            if data:
                id_subtitle_file = data[0].get('IDSubtitleFile')
            else:
                raise Exception(
                    "Could not find subtitles for {filename} and language {language}".format(
                        filename=filename, language=self.ost_language))

        self.ost.download_subtitles([id_subtitle_file], output_directory=self.dir_name, extension='srt')
        return os.path.join(self.dir_name, id_subtitle_file + '.srt')

    def find_imdb_id(self, filename):
        name_info = PTN.parse(filename)
        search = tmdb.Search()
        if name_info['season'] and name_info['episode']:
            response = search.tv(query=name_info['title'])
            tmdb_id = response['results'][0]['id']
            tv = tmdb.tv.TV_Episodes(tmdb_id, name_info['season'], name_info['episode'])
            return tv.external_ids()['imdb_id'][2:]
        else:
            if name_info['year']:
                response = search.movie(
                    query=name_info['title'],
                    year=name_info['year'],
                    append_to_response='external_ids')
            else:
                response = search.movie(
                    query=name_info['title'],
                    append_to_response='external_ids')
            return response.results[0]['id']


        # {
        #     'episode': 5,
        #     'season': 1,
        #     'title': 'Mr Robot',
        #     'codec': 'x264',
        #     'group':  'KILLERS[ettv]'
        #     'quality': 'HDTV'
        # }

        # {
        #     'group': '0-FGT',
        #     'title': 'The Martian',
        #     'resolution': '540p',
        #     'excess': ['KORSUB', '2'],
        #     'codec': 'x264',
        #     'year': 2015,
        #     'audio': 'AAC',
        #     'quality': 'HDRip'
        # }
