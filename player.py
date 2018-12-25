import glob
from collections import Counter


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
        stats = {
            "sr" : [],
            "win" : [],
            "hero" : [],
            "perf" : [],
            "time" : [],
            }

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
        hero_stats = {}
        all_heroes = set(self.stats["hero"])
        for hero in all_heroes:
            hero_stats[hero] = {
                "total_sr_gain" : 0,
                "played_games" : 0,
                "av_gain_per_game" : 0,
                "av_gain_av_loss" : [[0, 0], [0, 0]], #To be averaged
                "win_loss_ratio" : 0
                }
        for i, hero in enumerate(self.stats["hero"]):
            hero_stats[hero]["total_sr_gain"] += self.sr_change[i]
            hero_stats[hero]["played_games"] += 1
            if self.stats["win"]:
                index = 0
                hero_stats[hero]["win_loss_ratio"] += 1
            else:
                index = 1
            hero_stats[hero]["av_gain_av_loss"][index][0] += self.sr_change[i]
            hero_stats[hero]["av_gain_av_loss"][index][1] += 1

        for hero in hero_stats:
            hero_stats[hero]["win_loss_ratio"] = games / wins
            for i in range(2):
                ratio = hero_stats[hero]["av_gain_av_loss"][i]
                try:
                    average = ratio[0] / ratio[1]
                except ZeroDivisionError:
                    average = 0
                hero_stats[hero]["av_gain_av_loss"][i] = average
            played_games = hero_stats[hero]["played_games"]
            total_change = hero_stats[hero]["total_sr_gain"]
            hero_stats[hero]["av_gain_per_game"] = total_change / played_games

        return hero_stats










#Average SR Gain/Loss
#Season High
#Season Low
#All SR Over time
#Change in SR per game
#W/L
#Played Heroes frequency
#Which heroes played
#All stats by hero
#Best hero
#Self reported performance
#timelist
