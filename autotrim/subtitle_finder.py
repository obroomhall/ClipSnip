import os

import srt
from ffsubsync import subsync
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

from autotrim.filename_parser import ParsedMovie, ParsedSeries


class SubtitleFinder:

    def __init__(self, dir_name, ost_username, ost_password):
        self.ost = OpenSubtitles()
        self.ost.login(ost_username, ost_password)
        self.ost_language = 'eng'
        self.dir_name = dir_name
        self.subsync_parser = subsync.make_parser()

    def find(self, imdb_id, parsed_media):
        if imdb_id:
            return self.find_subtitles(
                imdbid=imdb_id)
        elif isinstance(parsed_media, ParsedMovie):
            return self.find_subtitles(
                query=parsed_media.title)
        elif isinstance(parsed_media, ParsedSeries):
            return self.find_subtitles(
                query=parsed_media.title,
                season=parsed_media.season,
                episode=parsed_media.episode)

    def find_subtitles_by_hash(self, source):
        f = File(source)
        return self.find_subtitles(moviehash=f.get_hash(), moviebytesize=f.size)

    def find_subtitles(self, **request):
        request.update(sublanguageid=self.ost_language)
        if 'imdbid' in request and request['imdbid'][:2] == 'tt':
            request.update(imdbid=request['imdbid'][2:])
        subs_data = self.ost.search_subtitles([request])
        return subs_data

    def download_subtitles(self, subs_data):
        id_subtitle_file = subs_data[0].get('IDSubtitleFile')
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
