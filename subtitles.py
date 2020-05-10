import os
import subprocess

from pythonopensubtitles.opensubtitles import OpenSubtitles
import srt
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser


ost_username = os.environ['ost_username']
ost_password = os.environ['ost_password']

ost = OpenSubtitles()
# ost.login(ost_username, ost_password)


class ExtractedSubtitles:

    def __init__(self, subs, previous_end_time, next_start_time):
        self.subs = subs
        self.previous_end_time = previous_end_time
        self.next_start_time = next_start_time


class Subtitles:

    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.schema = Schema(
            index=NUMERIC(stored=True),
            content=TEXT(stored=True))

    def download_subtitles(self, imdb_id):

        data = ost.search_subtitles([{
            'sublanguageid': 'eng',
            'imdbid': imdb_id,
        }])
        id_subtitle_file = data[0].get('IDSubtitleFile')

        ost.download_subtitles([id_subtitle_file], output_directory=self.dir_name, extension='srt')

    def sync_subtitles(self, video_filename, subs_filename):

        subtitles = read_subtitles(subs_filename)

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

        return read_subtitles(synced_subs_filename)

    def search_subtitles(self, subtitles, search_str):

        ix = create_in(self.dir_name, self.schema)
        ix_writer = ix.writer()
        for subtitle in subtitles:
            ix_writer.add_document(
                index=subtitle.index - 1,
                content=subtitle.content
            )
        ix_writer.commit()

        extracted = []
        with ix.searcher() as searcher:
            query = QueryParser('content', ix.schema).parse(search_str)
            results = searcher.search(query)
            max_idx = len(subtitles) - 1
            for result in results:
                index = result['index']
                extracted.append(ExtractedSubtitles(
                    [subtitles[index]],
                    None if index - 1 < 0 else subtitles[index - 1].end,
                    None if index + 1 > max_idx else subtitles[index + 1].start,
                ))

        return extracted


def read_subtitles(filename):
    with open(filename, 'r') as f:
        raw_subs = f.read()
        subtitle_generator = srt.parse(raw_subs)
        return list(subtitle_generator)
