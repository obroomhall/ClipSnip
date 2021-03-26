import tmdbsimple as tmdb

from clipsnip.filename_parser import ParsedMovie, ParsedSeries


class MediaSearcher:

    def __init__(self, api_key):
        tmdb.API_KEY = api_key
        self.tmdb_searcher = tmdb.Search()

    def search(self, parsed_media):
        if isinstance(parsed_media, ParsedMovie):
            return self.search_movie(
                parsed_media.title,
                parsed_media.year
            )
        elif isinstance(parsed_media, ParsedSeries):
            return self.search_tv(
                parsed_media.title,
                parsed_media.season,
                parsed_media.episode
            )

    def search_movie(self, title, year=None):
        if year:
            response = self.tmdb_searcher.movie(query=title, year=year)
            if 'results' not in response or not response['results']:
                response = self.tmdb_searcher.movie(query=title)
        else:
            response = self.tmdb_searcher.movie(query=title)

        tmdb_id = get_tmdb_id(response)
        movie = tmdb.movies.Movies(tmdb_id)
        return get_imdb_id(movie)

    def search_tv(self, title, season, episode):
        response = self.tmdb_searcher.tv(query=title)
        tmdb_id = get_tmdb_id(response)
        tv = tmdb.tv.TV_Episodes(tmdb_id, season, episode)
        return get_imdb_id(tv)


def get_tmdb_id(tmdb_search_response):
    try:
        return tmdb_search_response['results'][0]['id']
    except IndexError:
        raise IndexError("Could not find TMDb ID in response.")


def get_imdb_id(tmdb_find_response):
    try:
        return tmdb_find_response.external_ids()['imdb_id']
    except IndexError:
        raise IndexError("Could not find IMDb ID in response.")
