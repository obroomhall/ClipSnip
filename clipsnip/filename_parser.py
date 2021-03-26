import re


class ParsedMovie:
    def __init__(self, title, year):
        self.title = title
        self.year = year


class ParsedSeries:
    def __init__(self, title, season, episode):
        self.title = title
        self.season = season
        self.episode = episode


year_pattern = re.compile('[. ]\\(?(?P<year>(19|2\\d)\\d{2})\\)?[. ]')
season_episode_pattern = re.compile('[. ][Ss](?P<season>\\d{1,2})[Ee](?P<episode>\\d{1,2})[. ]')


def parse(filename):
    filename = filename.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
    year_matches = [(i.start(), i.group('year')) for i in year_pattern.finditer(filename)]
    if year_matches:
        year_match = year_matches[-1]
        title_end = year_match[0]
        year = int(year_match[1])
        title = get_title(filename, title_end)
        return ParsedMovie(title, year)
    else:
        tv_match = season_episode_pattern.search(filename)
        if tv_match:
            title_end = tv_match.start(0)
            season = int(tv_match.group('season'))
            episode = int(tv_match.group('episode'))
            title = get_title(filename, title_end)
            return ParsedSeries(title, season, episode)


def get_title(filename, end_index):
    if end_index is None:
        raw_title = filename
    else:
        raw_title = filename[:end_index]
    return raw_title.replace('.', ' ')
