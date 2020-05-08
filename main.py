import reddit
import subtitles
import gif
import sys


def main():

    source = 'test/Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv'

    # reddit.get_quote_candidates('dzsk34')
    # subtitles.download_subtitles('1467481')
    subtitle_list = subtitles.parse_subtitles('test/1952727133.srt', "hello")
    return_code = gif.extract_gif(source, subtitle_list)
    return return_code


sys.exit(main())
