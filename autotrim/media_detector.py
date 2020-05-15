import re


class MediaInfo:

    def __init__(self, title, is_movie, year=None, season=None, episode=None):
        self.title = title
        self.year = year
        self.season = season
        self.episode = episode
        self.is_movie = is_movie


year_pattern = re.compile('[. ]\\(?(?P<year>(19|2\\d)\\d{2})\\)?[. ]')
season_episode_pattern = re.compile('[. ][Ss](?P<season>\\d{1,2})[Ee][Pp]?(?P<episode>\\d{1,2})[. ]')


def parse(filename):

    year = None
    season = None
    episode = None

    year_matches = [(i.start(), i.group('year')) for i in year_pattern.finditer(filename)]
    if year_matches:
        year_match = year_matches[-1]
        title_end = year_match[0]
        year = year_match[1]
        is_movie = True
    else:
        tv_match = season_episode_pattern.search(filename)
        if tv_match:
            title_end = tv_match.start(0)
            season = tv_match.group('season')
            episode = tv_match.group('episode')
            is_movie = False
        else:
            raise ValueError("Could not detect media. Please specify an IMDb ID manually.")

    if title_end is None:
        raw_title = filename
    else:
        raw_title = filename[:title_end]

    title = raw_title.replace('.', ' ')
    return MediaInfo(title, is_movie, year, season, episode)
