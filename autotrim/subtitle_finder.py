from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import os
import srt
from ffsubsync import subsync

from autotrim import filename_parser
from autotrim.media_searcher import MediaSearcher
from autotrim.filename_parser import ParsedMovie,ParsedSeries
import autotrim.filename_parser


class SubtitleFinder:

    def __init__(self, dir_name, ost_username, ost_password, tmdb_key):
        self.ost = OpenSubtitles()
        self.login(ost_username, ost_password)
        self.ost_language = 'eng'
        self.dir_name = dir_name
        self.subsync_parser = subsync.make_parser()
        self.media_searcher = MediaSearcher(tmdb_key)

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
                parsed_media = filename_parser.parse(filename)
                if parsed_media is ParsedMovie:
                    imdb_id = self.media_searcher.search_movie(
                        parsed_media.title,
                        parsed_media.year
                    )
                else:
                    imdb_id = self.media_searcher.search_tv(
                        parsed_media.title,
                        parsed_media.season,
                        parsed_media.episode
                    )

                data = self.ost.search_subtitles([{
                    'sublanguageid': self.ost_language,
                    'imdbid': imdb_id,
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
