import argparse
import os
import shutil
from pathlib import Path

import pysubs2

from clipsnip.config import tmp_dir
from clipsnip.gif_extractor import GifExtractor
from clipsnip.quote import SubtitleExtractor
from clipsnip.subtitle import SubtitleFinder


def main():
    parser = get_parser()
    args = parser.parse_args()
    run(**vars(args))


def run(video_filename, quote, best_match=False, padding_seconds=1.5, skip_subsync=False,
        subtitles_filename=None, imdb_id=None, ost_username=None, ost_password=None, tmdb_key=None):

    Path(tmp_dir).mkdir(parents=True, exist_ok=True)

    try:
        if subtitles_filename is None:
            subtitle_finder = SubtitleFinder(skip_subsync, ost_username, ost_password, tmdb_key)
            subtitles = subtitle_finder.find_and_download(video_filename, imdb_id)
            if subtitles is None:
                raise LookupError("Could not find subtitles for file.")
        else:
            subtitles = pysubs2.load(subtitles_filename)

        subtitle_extractor = SubtitleExtractor()
        extracted_subs = subtitle_extractor.search_subtitles(subtitles, quote)

        if best_match:
            extracted_subs = [max(extracted_subs, key=lambda x:x.score)]

        gif_extractor = GifExtractor(padding_seconds)
        gif_extractor.extract_gif(video_filename, extracted_subs)
    finally:
        shutil.rmtree(tmp_dir)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.description = 'ClipSnip extracts relevant clips from a video based on your provided quote. Example usage: ' \
                         '{0} -v Forest.Gump.1994.1080p.mkv -q \'box of chocolates\''.format(parser.prog)
    parser.add_argument(
        '-v', '--video-filename',
        required=True,
        help='Path to a video file')
    parser.add_argument(
        '-q', '--quote',
        required=True,
        help='Quote to search for')
    parser.add_argument(
        '-b', '--best-match',
        action='store_true',
        help='Only export the clip with the highest match')
    parser.add_argument(
        '-i', '--imdb-id',
        help='Override IMDb id used to find subtitles')
    parser.add_argument(
        '-p', '--padding-seconds',
        default=1.5,
        help='Maximum seconds to trim before and after subtitles (default=1.5)')
    parser.add_argument(
        '--skip-subsync',
        action='store_true',
        help='Skip syncing subtitles to audio track')
    parser.add_argument(
        '-s', '--subtitles-filename',
        help='Use local subtitle file instead of finding one online')
    parser.add_argument(
        '--ost-username',
        default=os.environ.get('ost_username'),
        help='Username for grabbing subtitles from opensubtitles.org')
    parser.add_argument(
        '--ost-password',
        default=os.environ.get('ost_password'),
        help='Password for grabbing subtitles from opensubtitles.org')
    parser.add_argument(
        '--tmdb-key',
        default=os.environ.get('tmdb_key'),
        help='The Movie Database API key for resolving file names'
    )
    return parser


if __name__ == "__main__":
    main()
