import reddit
import subtitles
import gif
import sys


def godfather():
    source = 'D:/Videos/Media/The.Godfather.Part.I.The.Coppola.Restoration.1972.BluRay.1080p.TrueHD.5.1.AVC.REMUX-FraMeSToR\The.Godfather.Part.I.The.Coppola.Restoration.1972.BluRay.1080p.TrueHD.5.1.AVC.REMUX-FraMeSToR.mkv'
    subtitle_list = subtitles.parse_subtitles(
        source,
        "D:\Videos\Media\The.Godfather.Part.I.The.Coppola.Restoration.1972.BluRay.1080p.TrueHD.5.1.AVC.REMUX-FraMeSToR\The.Godfather.Part.I.1972.720p.BluRay.x264-ADHD.Subs.EN-HI.srt",
        "even think to call me godfather")
    gif.extract_gif(source, subtitle_list)


def community():
    source = 'test/Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv'
    # reddit.get_quote_candidates('dzsk34')
    # subtitles.download_subtitles('1467481')
    subtitle_list = subtitles.parse_subtitles(
        source,
        'test/1952727133.srt',
        "wish"
    )
    gif.extract_gif(source, subtitle_list)


def main():
    # godfather()
    community()


main()
