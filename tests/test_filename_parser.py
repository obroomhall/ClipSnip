import autotrim.filename_parser as parser
import tests.candidates as candidates
import unittest


class FilenameParserTest(unittest.TestCase):

    def test_parse_movies(self):

        for candidate in candidates.get_movie_candidates():
            parsed = parser.parse(candidate.filename)
            self.assertTrue(parsed.title.startswith(candidate.title))
            self.assertEqual(int(parsed.year), candidate.year)

    def test_parse_tv(self):

        for candidate in candidates.get_tv_candidates():
            parsed = parser.parse(candidate.filename)
            self.assertTrue(parsed.title.startswith(candidate.title))
            self.assertEqual(int(parsed.season), candidate.season)
            self.assertEqual(int(parsed.episode), candidate.episode)

    def test_not_parse_tv(self):

        for filename in candidates.get_bad_tv_candidates():
            parsed = parser.parse(filename)
            self.assertIsNone(parsed)
