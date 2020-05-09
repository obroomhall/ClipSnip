import os
import subprocess
import tempfile

from pythonopensubtitles.opensubtitles import OpenSubtitles
import srt
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from subsync import subsync


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


def read_subtitles(filename):
    with open(filename, 'r') as f:
        raw_subs = f.read()
        subtitle_generator = srt.parse(raw_subs)
        return list(subtitle_generator)


def parse_subtitles(video_filename, subs_filename, search_str):

    subtitles = read_subtitles(subs_filename)

    tmp_dir = tempfile.TemporaryDirectory()

    encoded_subs_filename = os.path.join(tmp_dir.name, 'encoded.srt')
    with open(encoded_subs_filename, 'w') as f:
        f.write(srt.compose(subtitles))

    synced_subs_filename = os.path.join(tmp_dir.name, 'synced.srt')
    subprocess.run([
        'subsync',
        video_filename,
        '-i', encoded_subs_filename,
        '-o', synced_subs_filename
    ], check=True)

    synced_subtitles = read_subtitles(synced_subs_filename)

    schema = Schema(
        index=NUMERIC(stored=True),
        content=TEXT(stored=True)
    )

    ix = create_in(tmp_dir.name, schema)
    ix_writer = ix.writer()
    for subtitle in synced_subtitles:
        ix_writer.add_document(
            index=subtitle.index-1,
            content=subtitle.content
        )
    ix_writer.commit()

    extracted = []
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(search_str)
        results = searcher.search(query)
        for result in results:
            index = result['index']
            extracted.append(synced_subtitles[index])

    return extracted
