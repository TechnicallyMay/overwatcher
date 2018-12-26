import glob
from collections import Counter, defaultdict


class Player():

    def __init__(self, name, start_SR=None):
        self.name = name
        self.file_name = 'data\players\%s.txt' % name
        if start_SR:
            with open(self.file_name, "w+") as new_player:
                new_player.write(str(start_SR))
                new_player.close()
        self.stats = self.get_stats()
        self.sr_change = self.sr_change_per_game()
        self.main_hero = self.most_played_hero()
        self.hero_stats = self.hero_stats_per_game()


    def get_stats(self):
        stats = defaultdict(list)
        
        with open (self.file_name, "r") as games:
            for i, game in enumerate(games):
                game_stats = game.split()
                if game_stats[0].isdigit():
                    stats["sr"].append(int(game_stats[0]))
                else:
                    win = game_stats[0] == 'W'
                    stats["win"].append(win)
                    stats["sr"].append(int(game_stats[1]))
                    stats["hero"].append(game_stats[2])
                    stats["perf"].append(int(game_stats[3]))
                    time = [int(x) for x in game_stats[4:]]
                    stats["time"].append(time)

        return stats


    def most_played_hero(self):
        count = Counter(self.stats["hero"])
        return count.most_common(1)[0][0]


    def sr_change_per_game(self):
        sr_change = []
        for i in range(1, len(self.stats["sr"])):
            sr_change.append(self.stats["sr"][i] - self.stats["sr"][i-1])
        return sr_change


    def hero_stats_per_game(self):
        hero_stats = defaultdict(lambda: defaultdict(int))

        for i, hero in enumerate(self.stats["hero"]):
            sr_change = self.sr_change[i]
            hero_stats[hero]["total_change"] += sr_change
            hero_stats[hero]["played_games"] += 1
            if self.stats["win"][i]:
                hero_stats[hero]["wins"] += 1
                hero_stats[hero]["total_gained"] += sr_change
            else:
                hero_stats[hero]["total_lost"] += sr_change
        ranked_stats = self.rank_heroes(hero_stats)

        return ranked_stats


    def rank_heroes(self, stats):
        ranking = []
        for hero, values in stats.items():
            try:
                av_change = values["total_change"] / values["played_games"]
            except ZeroDivisionError:
                av_change = 0
            stats[hero]["av_change"] = av_change
            ranking.append((av_change, hero))

        sorted_rank = sorted(ranking, reverse=True)
        for i in range(len(sorted_rank)):
            stats[sorted_rank[i][1]]["rank"] = i +1

        return stats
