import unittest

import clipsnip.filename_parser as parser
import tests.candidates as candidates


class FilenameParserTest(unittest.TestCase):

    def test_parse_movies(self):

        for candidate in candidates.get_movie_candidates():
            with self.subTest(candidate.title):
                parsed = parser.parse(candidate.filename)
                self.assertTrue(parsed.title.startswith(candidate.title))
                self.assertEqual(parsed.year, candidate.year)

    def test_parse_tv(self):

        for candidate in candidates.get_tv_candidates():
            with self.subTest(candidate.title):
                parsed = parser.parse(candidate.filename)
                self.assertTrue(parsed.title.startswith(candidate.title))
                self.assertEqual(parsed.season, candidate.season)
                self.assertEqual(parsed.episode, candidate.episode)

    def test_not_parse_tv(self):

        for i, filename in enumerate(candidates.get_bad_tv_candidates()):
            with self.subTest(i=i):
                parsed = parser.parse(filename)
                self.assertIsNone(parsed, filename)


if __name__ == '__main__':
    unittest.main()
