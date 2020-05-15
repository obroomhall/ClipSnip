import autotrim.media_detector as parser
import unittest


class MediaDetectorTest(unittest.TestCase):

    def test_parse_movies(self):

        candidates = [
            ('12.Angry.Men.1957.1080p.BluRay.x264-CiNEFiLE',
             '12 Angry Men', 1957),
            ('2001.A.Space.Odyssey.1968.1080p.BluRay.x264-HaB.mkv',
             '2001 A Space Odyssey', 1968),
            ('3.Idiots.2009.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-RK.mkv',
             '3 Idiots', 2009),
            ('Chronicle.DC.2012.Blu-Ray.1080p.DTS-HDMA5.1.x264.dxva-FraMeSToR',
             'Chronicle', 2012),
            ('Grease.(1978).1080p.UHD.BluRay.DD5.1.HDR.x265-DON.mkv',
             'Grease', 1978),
            ('John Wick 2014 Bluray 1080p DTS-HD-7 1 x264-Grym',
             'John Wick', 2014),
            ('John.Wick.Chapter.2.2017.PROPER.1080p.UHD.BluRay.DD+7.1.HDR.x265-CtrlHD.mkv',
             'John Wick Chapter 2', 2017),
            ('John.Wick.Chapter.3.Parabellum.2019.1080p.BluRay.DD-EX.5.1.x264-iFT',
             'John Wick Chapter 3 Parabellum', 2019),
            ('Mamma.Mia!.2008.BluRay.1080p.DTS.x264.dxva-EuReKA.mkv',
             'Mamma Mia!', 2008),
            ('spider-man.far.from.home.2019.1080p.bluray.x264-sparks.mkv',
             'spider-man far from home', 2019),
            ('The.Godfather.Part.II.The.Coppola.Restoration.1974.BluRay.1080p.TrueHD.5.1.AVC.REMUX-FraMeSToR',
             'The Godfather Part II', 1974),
            ('White.Chicks.UNRATED.2004.1080p.NF.WEBRip.DD5.1.x264-monkee.mkv',
             'White Chicks', 2004),
        ]

        for (filename, title, year) in candidates:
            parsed = parser.parse(filename)
            self.assertTrue(parsed.title.startswith(title))
            self.assertEqual(int(parsed.year), year)

    def test_parse_tv(self):

        candidates = [
            ('Black.Mirror.S02E01.1080p.BluRay.x264-FilmHD.mkv',
             'Black Mirror', 2, 1),
            ('Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv',
             'Community', 1, 1),
            ('Family.Guy.S12E01.Finders.Keepers.1080p.WEB-DL.DD5.1.H.264-CtrlHD.mkv',
             'Family Guy', 12, 1),
            ('Mad.Men.S01E01.BluRay.1080p.x264.H@M.mkv',
             'Mad Men', 1, 1),
            ('La.Casa.de.Papel.S01E01.1080p.NF.WEB-DL.DDP2.0.x264-Mooi1990.mkv',
             'La Casa de Papel', 1, 1),
            ('Ozark.S03E01.Wartime.1080p.NF.WEB-DL.DDP5.1.x264-NTb.mkv',
             'Ozark', 3, 1),
            ('Star.Wars.The.Clone.Wars.S01E11.Dooku.Captured.1080p.BluRay.REMUX.VC-1.DD.5.1-EPSiLON.mkv',
             'Star Wars The Clone Wars', 1, 11),
            ('Rick.and.Morty.S04E06.Never.Ricking.Morty.1080p.AMZN.WEB-DL.DD+5.1.H.264-CtrlHD.mkv',
             'Rick and Morty', 4, 6),
            ('The.Rookie.S01E18.Homefront.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv',
             'The Rookie', 1, 18),
            ('Westworld.S03E07.Passed.Pawn.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv',
             'Westworld', 3, 7),
        ]

        for (filename, title, season, episode) in candidates:
            parsed = parser.parse(filename)
            self.assertTrue(parsed.title.startswith(title))
            self.assertEqual(int(parsed.season), season)
            self.assertEqual(int(parsed.episode), episode)

    def test_not_parse_tv(self):

        bad_candidates = [
            'Black.Mirror.S02.Special.White.Christmas.1080p.WEB-DL.DD2.0.H.264-CasStudio.mkv',
        ]

        for filename in bad_candidates:
            self.assertRaises(ValueError, parser.parse, filename)
