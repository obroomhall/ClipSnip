import os
from pythonopensubtitles.opensubtitles import OpenSubtitles
import srt
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

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


def parse_subtitles(filename, search_str):
    f = open(filename, "r")
    subtitle_generator = srt.parse(f.read())
    subtitles = list(subtitle_generator)

    schema = Schema(
        index=NUMERIC(stored=True),
        start=KEYWORD(stored=True),
        end=KEYWORD(stored=True),
        content=TEXT(stored=True)
    )
    ix = create_in('indexdir', schema)
    writer = ix.writer()
    for subtitle in subtitles:
        writer.add_document(
            index=subtitle.index-1,
            start=str(subtitle.start),
            end=str(subtitle.end),
            content=subtitle.content
        )
    writer.commit()

    extracted = []
    with ix.searcher() as searcher:
        query = QueryParser('content', ix.schema).parse(search_str)
        results = searcher.search(query)
        for result in results:
            extracted.append(subtitles[result['index']])

    return extracted
