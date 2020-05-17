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

    def __init__(self, dir_name, ost_username, ost_password):
        self.ost = OpenSubtitles()
        self.ost.login(ost_username, ost_password)
        self.ost_language = 'eng'
        self.dir_name = dir_name
        self.subsync_parser = subsync.make_parser()

    def download_subtitles_by_hash(self, source):
        f = File(source)
        subs_data = self.ost.search_subtitles([{
            'sublanguageid': self.ost_language,
            'moviehash': f.get_hash(),
            'moviebytesize': f.size
        }])
        if subs_data:
            return self.download_subtitles(subs_data)

    def download_subtitles_by_id(self, imdb_id):
        subs_data = self.ost.search_subtitles([{
            'sublanguageid': self.ost_language,
            'imdbid': imdb_id,
        }])
        if subs_data:
            return self.download_subtitles(subs_data)

    def download_subtitles(self, data):
        id_subtitle_file = data[0].get('IDSubtitleFile')
        self.ost.download_subtitles([id_subtitle_file], output_directory=self.dir_name)
        subtitle_filename = os.path.join(self.dir_name, id_subtitle_file + '.srt')
        return subtitle_filename

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
