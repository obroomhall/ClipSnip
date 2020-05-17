class MovieCandidate:

    def __init__(self, filename, title, tmdb_id, imdb_id, year):
        self.filename = filename
        self.title = title
        self.tmdb_id = tmdb_id
        self.imdb_id = imdb_id
        self.year = year


class TVCandidate:

    def __init__(self, filename, title, tmdb_id, imdb_id, season, episode):
        self.filename = filename
        self.title = title
        self.tmdb_id = tmdb_id
        self.imdb_id = imdb_id
        self.season = season
        self.episode = episode


def get_movie_candidates():
    return [
        MovieCandidate(
            '12.Angry.Men.1957.1080p.BluRay.x264-CiNEFiLE',
            '12 Angry Men', 389, 'tt0050083', 1957),
        MovieCandidate(
            '2001.A.Space.Odyssey.1968.1080p.BluRay.x264-HaB.mkv',
            '2001 A Space Odyssey', 62, 'tt0062622', 1968),
        MovieCandidate(
            '3.Idiots.2009.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-RK.mkv',
            '3 Idiots', 20453, 'tt1187043', 2009),
        MovieCandidate(
            'Chronicle.DC.2012.Blu-Ray.1080p.DTS-HDMA5.1.x264.dxva-FraMeSToR',
            'Chronicle', 76726, 'tt1706593', 2012),
        MovieCandidate(
            'Grease.(1978).1080p.UHD.BluRay.DD5.1.HDR.x265-DON.mkv',
            'Grease', 621, 'tt0077631', 1978),
        MovieCandidate(
            'John Wick 2014 Bluray 1080p DTS-HD-7 1 x264-Grym',
            'John Wick', 245891, 'tt2911666', 2014),
        MovieCandidate(
            'John.Wick.Chapter.2.2017.PROPER.1080p.UHD.BluRay.DD+7.1.HDR.x265-CtrlHD.mkv',
            'John Wick Chapter 2', 324552, 'tt4425200', 2017),
        MovieCandidate(
            'John.Wick.Chapter.3.Parabellum.2019.1080p.BluRay.DD-EX.5.1.x264-iFT',
            'John Wick Chapter 3 Parabellum', 458156, 'tt6146586', 2019),
        MovieCandidate(
            'Mamma.Mia!.2008.BluRay.1080p.DTS.x264.dxva-EuReKA.mkv',
            'Mamma Mia!', 11631, 'tt0795421', 2008),
        MovieCandidate(
            'spider-man.far.from.home.2019.1080p.bluray.x264-sparks.mkv',
            'spider-man far from home', 429617, 'tt6320628', 2019),
        MovieCandidate(
            'The.Godfather.Part.II.The.Coppola.Restoration.1974.BluRay.1080p.TrueHD.5.1.AVC.REMUX-FraMeSToR',
            'The Godfather Part II', 240, 'tt0071562', 1974),
        MovieCandidate(
            'White.Chicks.UNRATED.2004.1080p.NF.WEBRip.DD5.1.x264-monkee.mkv',
            'White Chicks', 12153, 'tt0381707', 2004),
    ]


def get_tv_candidates():
    return [
        TVCandidate(
            'Black.Mirror.S02E01.1080p.BluRay.x264-FilmHD.mkv',
            'Black Mirror', 42009, 'tt2290780', 2, 1),
        TVCandidate(
            'Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv',
            'Community', 18347, 'tt1467481', 1, 1),
        TVCandidate(
            'Family.Guy.S12E01.Finders.Keepers.1080p.WEB-DL.DD5.1.H.264-CtrlHD.mkv',
            'Family Guy', 1434, 'tt2913958', 12, 1),
        TVCandidate(
            'La.Casa.de.Papel.S01E01.1080p.NF.WEB-DL.DDP2.0.x264-Mooi1990.mkv',
            'La Casa de Papel', 71446, 'tt6807344', 1, 1),
        TVCandidate(
            'Star.Wars.The.Clone.Wars.S01E11.Dooku.Captured.1080p.BluRay.REMUX.VC-1.DD.5.1-EPSiLON.mkv',
            'Star Wars The Clone Wars', 12180, 'tt1322835', 1, 11),
        TVCandidate(
            'Rick.and.Morty.S04E06.Never.Ricking.Morty.1080p.AMZN.WEB-DL.DD+5.1.H.264-CtrlHD.mkv',
            'Rick and Morty', 60625, 'tt10655686', 4, 6),
        TVCandidate(
            'The.Rookie.S01E18.Homefront.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv',
            'The Rookie', 79744, 'tt9256660', 1, 18),
        TVCandidate(
            'Westworld.S03E07.Passed.Pawn.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv',
            'Westworld', 63247, 'tt10011158', 3, 7),
        # These shows have no IMDb ID attached to them in TMDb, which shows their database is incomplete. OpenSubtitles
        # only accepts
        # TVCandidate(
        #     'Mad.Men.S01E01.BluRay.1080p.x264.H@M.mkv',
        #     'Mad Men', 1104, 'tt1059578', 1, 1),
        # TVCandidate(
        #     'Ozark.S03E01.Wartime.1080p.NF.WEB-DL.DDP5.1.x264-NTb.mkv',
        #     'Ozark', 69740, 'tt9108660', 3, 1),
    ]


def get_bad_tv_candidates():
    return [
        'Black.Mirror.S02.Special.White.Christmas.1080p.WEB-DL.DD2.0.H.264-CasStudio.mkv',
    ]
