import reddit
from subtitle_finder import SubtitleFinder
from subtitle_extractor import SubtitleExtractor
from gif_extractor import GifExtractor


def main():
    source = 'test/Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv'
    tmp_dir = 'test/data/'
    # reddit.get_quote_candidates('dzsk34')

    subtitle_finder = SubtitleFinder(tmp_dir)
    subs = subtitle_finder.download_subtitles(source)

    subtitle_extractor = SubtitleExtractor(tmp_dir)
    synced_subs = subtitle_extractor.sync_subtitles(source, subs)
    extracted_subs = subtitle_extractor.search_subtitles(synced_subs, "cool")

    gif_extractor = GifExtractor(tmp_dir)
    gif_extractor.extract_gif(source, extracted_subs)


main()
