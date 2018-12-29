import unittest
from main import player


class PlayerDataTestCase(unittest.TestCase):

    def setUp(self):
        self.player = player.Player("testing_data")
        self.player.activate()


    def tearDown(self):
        self.player.deactivate()
        self.player = None


class PlayerDataTestProperties(PlayerDataTestCase):

    def test_stats(self):
        stats = self.player.stats
        self.assertEqual(stats["win"], [False, False, False, False, True],
        "Incorrect win list")
        self.assertEqual(stats["sr"], [1582, 1561, 1534, 1512, 1487, 1511],
        "Incorrect SR list")
        self.assertEqual(stats["hero"], ["Winston","D.Va","D.Va","Winston","Winston"],
        "Incorrect hero list")
        self.assertEqual(stats["perf"], [5, 1, 1, 2, 9],
        "Incorrect performance list")
        self.assertEqual(stats["time"],
        [
        [0, 30, 2000, 24, 27],
        [5, 20, 2009, 22, 57],
        [7, 18, 2014, 16, 53],
        [2, 19, 2016, 10, 42],
        [1, 18, 2013, 14, 44]
        ],
        "Incorrect time list"
        )


    def test_sr_change_per_game(self):
        self.assertEqual(self.player.sr_change, [-21, -27, -22, -25, 24],
        "Incorrect SR change list")


    def test_most_played_hero(self):
        self.assertEqual(self.player.main_hero, "Winston",
                        "Incorrect most played hero")


    def test_hero_stats(self):
        stats = self.player.hero_stats["D.Va"]
        self.assertEqual(stats["total_change"], -49,
                        "D.Va total_change incorrect")
        self.assertEqual(stats["played_games"], 2,
                        "D.Va played_games incorrect")
        self.assertEqual(stats["wins"], 0,
                        "D.Va wins incorrect")
        self.assertEqual(stats["total_gained"], 0,
                        "D.Va total_gained incorrect")
        self.assertEqual(stats["total_lost"], 49,
                        "D.Va total_lost incorrect")
        self.assertEqual(stats["av_change"], -24.5,
                        "D.Va av_change incorrect")
        self.assertEqual(stats["rank"], 2,
                        "D.Va rank incorrect")
