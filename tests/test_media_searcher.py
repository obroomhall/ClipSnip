import tests.candidates as candidates
from autotrim.media_searcher import MediaSearcher
import unittest
import os


class MediaSearcherTest(unittest.TestCase):

    def setUp(self):
        self.searcher = MediaSearcher(os.getenv('tmdb_key'))

    def test_search_movies(self):
        for candidate in candidates.get_movie_candidates():
            with self.subTest(candidate.title):
                imdb_id = self.searcher.search_movie(candidate.title, candidate.year)
                self.assertEqual(imdb_id, candidate.imdb_id)

    def test_search_series(self):
        for candidate in candidates.get_tv_candidates():
            with self.subTest(candidate.title):
                imdb_id = self.searcher.search_tv(candidate.title, candidate.season, candidate.episode)
                self.assertEqual(imdb_id, candidate.imdb_id)


if __name__ == '__main__':
    unittest.main()
