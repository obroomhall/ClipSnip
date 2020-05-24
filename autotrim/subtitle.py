
import tempfile

import srt
from ffsubsync import subsync
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

from autotrim import filename_parser
from autotrim.filename_parser import ParsedMovie, ParsedSeries
from autotrim.media_searcher import MediaSearcher


class SubtitleFinder:

    def __init__(self, skip_subsync, ost_username, ost_password, tmdb_key):
        self.skip_subsync = skip_subsync
        self.ost = OpenSubtitles()
        self.ost.login(ost_username, ost_password)
        self.ost_language = 'eng'
        if tmdb_key:
            self.media_searcher = MediaSearcher(tmdb_key)
        if not self.skip_subsync:
            self.subsync_parser = subsync.make_parser()

    def find_and_download(self, source, imdb_id):

        # subtitles matching on hash are already synced
        subs_data = self.find_subtitles_by_hash(source)
        if subs_data:
            return self.download_subtitles(subs_data)

        parsed_media = filename_parser.parse(source)
        if imdb_id is None and self.media_searcher is not None:
            imdb_id = self.media_searcher.search(parsed_media)

        if imdb_id is not None:
            subs_data = self.find_subtitles_by_id(imdb_id)
        elif isinstance(parsed_media, ParsedMovie):
            subs_data = self.find_subtitles_for_movie(parsed_media.title)
        elif isinstance(parsed_media, ParsedSeries):
            subs_data = self.find_subtitles_for_episode(parsed_media.title, parsed_media.season, parsed_media.episode)

        # sync subs unless explicitly asked not to
        if subs_data is not None:
            subs = self.download_subtitles(subs_data)
            if self.skip_subsync:
                return subs
            else:
                return self.sync_subtitles(source, subs)

    def find_subtitles_by_hash(self, source):
        f = File(source)
        return self.find_subtitles(moviehash=f.get_hash(), moviebytesize=f.size)

    def find_subtitles_by_id(self, imdb_id):
        return self.find_subtitles(imdbid=imdb_id)

    def find_subtitles_for_movie(self, title):
        return self.find_subtitles(query=title)

    def find_subtitles_for_episode(self, title, season, episode):
        return self.find_subtitles(query=title, season=season, episode=episode)

    def find_subtitles(self, **request):
        request.update(sublanguageid=self.ost_language)
        if 'imdbid' in request and request['imdbid'][:2] == 'tt':
            request.update(imdbid=request['imdbid'][2:])
        subs_data = self.ost.search_subtitles([request])
        return subs_data

    def download_subtitles(self, subs_data):
        id_subtitle_file = subs_data[0].get('IDSubtitleFile')
        subs_dict = self.ost.download_subtitles([id_subtitle_file], return_decoded_data=True)
        raw_subs = subs_dict.get(id_subtitle_file)
        return list(srt.parse(raw_subs))

    def sync_subtitles(self, video_filename, subtitles):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.srt') as tmp_unsynced:
            tmp_unsynced.write(srt.compose(subtitles).encode())
            tmp_unsynced.close()
            with tempfile.NamedTemporaryFile(suffix='.srt') as tmp_synced:
                tmp_synced.close()
                self.run_subsync(video_filename, tmp_unsynced.name, tmp_synced.name)
                return read_subtitles(tmp_synced.name)

    def run_subsync(self, reference, srtin, srtout):
        subsync.run(self.subsync_parser.parse_args([
            reference,
            '-i', srtin,
            '-o', srtout
        ]))


def read_subtitles(filename):
    with open(filename, 'r') as f:
        raw_subs = f.read()
        subtitle_generator = srt.parse(raw_subs)
        return list(subtitle_generator)
