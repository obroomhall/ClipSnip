import argparse
import os
from pathlib import Path

import autotrim.subtitle.io as sub_io
import autotrim.subtitle.sync as sub_sync
from autotrim import filename_parser
from autotrim.gif_extractor import GifExtractor
from autotrim.media_searcher import MediaSearcher
from autotrim.subtitle.find import SubtitleFinder
from autotrim.subtitle.search import SubtitleExtractor


def main():
    parser = get_parser()
    args = parser.parse_args()
    run(**vars(args))


def run(video_filename, quote, best_match=False, padding_seconds=1.5, skip_subsync=False,
        subtitles_filename=None, imdb_id=None, ost_username=None, ost_password=None, tmdb_key=None):

    tmp_dir = '.tmp/'
    Path(tmp_dir).mkdir(parents=True, exist_ok=True)

    subtitles_synced = False
    if not subtitles_filename:
        (subtitles_filename, subtitles_synced) = \
            find_subtitles(video_filename, imdb_id, tmp_dir, ost_username, ost_password, tmdb_key)

    if not subtitles_synced and not skip_subsync:
        subtitles_filename = sub_sync.sync_subtitles(video_filename, subtitles_filename, tmp_dir)

    subtitles = sub_io.read_subtitles(subtitles_filename)

    subtitle_extractor = SubtitleExtractor(tmp_dir)
    extracted_subs = subtitle_extractor.search_subtitles(subtitles, quote)

    if best_match:
        extracted_subs = [max(extracted_subs, key=lambda x:x.score)]

    gif_extractor = GifExtractor(tmp_dir, padding_seconds)
    gif_extractor.extract_gif(video_filename, extracted_subs)

    # Path(tmp_dir).rmdir()


def find_subtitles(video_filename, imdb_id, tmp_dir, ost_username, ost_password, tmdb_key):

    subtitle_finder = SubtitleFinder(tmp_dir, ost_username, ost_password)

    subtitles_synced = False
    subs_data = subtitle_finder.find_subtitles_by_hash(video_filename)
    if subs_data:
        subtitles_synced = True
    else:
        if imdb_id:
            subs_data = subtitle_finder.find_subtitles(imdbid=imdb_id)
        else:
            parsed_media = filename_parser.parse(video_filename)
            media_searcher = MediaSearcher(tmdb_key)
            imdb_id = media_searcher.search(parsed_media)
            subs_data = subtitle_finder.find(imdb_id, parsed_media)

    if subs_data:
        return subtitle_finder.download_subtitles(subs_data), subtitles_synced
    else:
        raise LookupError("Could not find subtitles for file.")


def get_parser():
    parser = argparse.ArgumentParser()
    parser.description = 'AutoTrim extracts relevant clips from a video based on your provided quote. Example usage: ' \
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
