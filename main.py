import reddit
from subtitle_extractor import SubtitleExtractor
from gif_extractor import GifExtractor


def main():
    source = 'test/Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv'
    subs = 'test/1952727133.srt'
    tmp_dir = 'test/data/'
    # reddit.get_quote_candidates('dzsk34')
    # subtitles.download_subtitles('1467481')

    subtitle_extractor = SubtitleExtractor(tmp_dir)
    synced_subs = subtitle_extractor.sync_subtitles(source, subs)
    extracted_subs = subtitle_extractor.search_subtitles(synced_subs, "cool")

    gif_extractor = GifExtractor(tmp_dir)
    gif_extractor.extract_gif(source, extracted_subs)


main()
