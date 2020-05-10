import reddit
from subtitles import Subtitles
from gif import GifExtractor


def main():
    source = 'test/Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv'
    subs = 'test/1952727133.srt'
    tmp_dir = 'test/data/'
    # reddit.get_quote_candidates('dzsk34')
    # subtitles.download_subtitles('1467481')

    subtitles = Subtitles(tmp_dir)
    synced_subs = subtitles.sync_subtitles(source, subs)
    extracted_subs = subtitles.search_subtitles(synced_subs, "nicest")

    gif_extractor = GifExtractor(tmp_dir)
    gif_extractor.extract_gif(source, extracted_subs)


main()
