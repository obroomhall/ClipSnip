from autogif.subtitle_finder import SubtitleFinder
from autogif.subtitle_extractor import SubtitleExtractor
from autogif.gif_extractor import GifExtractor
import argparse
import sys
import logging
from pathlib import Path


def main(cmd_args):
    try:
        run(cmd_args)
    except Exception as e:
        if cmd_args.debug:
            raise e
        else:
            logging.error(e)
        sys.exit(1)


def run(cmd_args):

    tmp_dir = '.tmp/'
    Path(tmp_dir).mkdir(parents=True, exist_ok=True)

    subtitle_finder = SubtitleFinder(tmp_dir)
    if cmd_args.subtitle:
        subtitles_filename = cmd_args.subtitle
        subtitles_synced = False
    else:
        [subtitles_filename, subtitles_synced] = subtitle_finder.download_subtitles(cmd_args.video, cmd_args.imdb_id)

    if not subtitles_synced and not cmd_args.skip_subsync:
        subtitles_filename = subtitle_finder.sync_subtitles(cmd_args.video, subtitles_filename)

    subtitles = subtitle_finder.read_subtitles(subtitles_filename)

    subtitle_extractor = SubtitleExtractor(tmp_dir)
    extracted_subs = subtitle_extractor.search_subtitles(subtitles, cmd_args.quote)

    if cmd_args.best_match:
        extracted_subs = [max(extracted_subs, key=lambda x:x.score)]

    gif_extractor = GifExtractor(tmp_dir)
    gif_extractor.extract_gif(cmd_args.video, extracted_subs)


def args():
    parser = argparse.ArgumentParser()
    parser.description = 'AutoGIF extracts relevant clips from a video based on your provided quote. Example usage: ' \
                         '{0} -v Forest.Gump.1994.1080p.mkv -q \'box of chocolates\''.format(parser.prog)
    parser.add_argument('-v', '--video', type=str,
                        help='Path to a video file', required=True)
    parser.add_argument('-q', '--quote', type=str,
                        help='Quote to search for', required=True)
    parser.add_argument('-b', '--best-match', action='store_true',
                        help='Only export the clip with the highest match')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show debugging output')
    parser.add_argument('-i', '--imdb-id', type=str,
                        help='Override IMDb id used to find subtitles')
    parser.add_argument('-o', '--output-format', type=str, default='mp4',
                        help='Output clip format (default=mp4)')
    parser.add_argument('-sk', '--skip-subsync', action='store_true',
                        help='Skip syncing subtitles to audio track')
    parser.add_argument('-sub', '--subtitle', type=str,
                        help='Use local subtitle file instead of finding one online')
    return parser.parse_args()


if __name__ == "__main__":
    main(args())
