from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from operator import itemgetter


class ExtractedSubtitles:

    def __init__(self, subs, score, previous_end_time, next_start_time):
        self.subs = subs
        self.score = score
        self.previous_end_time = previous_end_time
        self.next_start_time = next_start_time


class SubtitleExtractor:

    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.schema = Schema(
            index=NUMERIC(stored=True),
            content=TEXT(stored=True))

    def search_subtitles(self, subtitles, search_str, best_match=False):

        ix = create_in(self.dir_name, self.schema)
        ix_writer = ix.writer()
        for subtitle in subtitles:
            ix_writer.add_document(
                index=subtitle.index - 1,
                content=subtitle.content
            )
        ix_writer.commit()

        with ix.searcher() as searcher:

            query = QueryParser('content', ix.schema).parse(search_str)
            results = searcher.search(query)
            sorted_results = sorted(results, key=itemgetter('index'))

            max_idx = len(subtitles) - 1
            extracted = []
            i = 0
            while i < len(sorted_results):

                score = 0
                subs = []
                while i+len(subs) < len(sorted_results) \
                        and sorted_results[i+len(subs)]['index'] == sorted_results[i]['index']+len(subs):
                    score = max(score, sorted_results[i+len(subs)].score)
                    subs.append(subtitles[sorted_results[i+len(subs)]['index']])

                lower_index = sorted_results[i]['index']
                upper_index = sorted_results[i+len(subs)-1]['index']
                extracted.append(ExtractedSubtitles(
                    subs,
                    score,
                    None if lower_index - 1 < 0 else subtitles[lower_index - 1].end,
                    None if upper_index + 1 > max_idx else subtitles[upper_index + 1].start,
                ))

                i += len(subs)

        return extracted