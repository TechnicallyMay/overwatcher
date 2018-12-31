import glob
import sqlite3
from collections import Counter, defaultdict


class Player():

    def __init__(self, name, start_SR=None):
        self.name = name
        self.open_db()
        if start_SR:
            command = """INSERT INTO players (name, placed_sr)
                         VALUES (?, ?)"""
            self.crsr.execute(command, [name, start_SR])
        self.crsr.execute("SELECT id FROM players WHERE name = ?", (name,))
        self.id = self.crsr.fetchone()[0]
        print(self.name,self.id)
        self.close_db()
        self.active = False


    def activate(self):
        self.active = True
        self.stats = self.get_stats()
        if len(self.stats) > 1:
            self.sr_change = self.sr_change_per_game()
            self.hero_stats = self.hero_stats_per_game()
            self.main_hero = self.most_played_hero()
            self.best_hero = self.get_best_hero()
            self.av_gain_loss = self.get_gain_loss()


    def deactivate(self):
        self.active = False
        try:
            del(self.stats)
            del(self.sr_change)
            del(self.hero_stats)
            del(self.main_hero)
            del(self.best_hero)
            del(self.av_gain_loss)
        except AttributeError:
            pass


    def open_db(self):
        self.conn = sqlite3.connect('../data/players/player_data.db')
        self.crsr = self.conn.cursor();


    def close_db(self):
        self.conn.commit()
        self.conn.close()


    def get_stats(self):
        stats = defaultdict(list)
        self.open_db()
        command = """SELECT *
                     FROM games
                     WHERE player_id = ?"""
        for line in self.crsr.execute(command, (self.id,)):
            stats["sr"].append(line[1])
            stats["hero"].append(line[2])
            stats["performance"].append(line[3])
            stats["time"].append(line[4])
        self.close_db()
        return stats


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
                hero_stats[hero]["total_lost"] += abs(sr_change)
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
            stats[sorted_rank[i][1]]["rank"] = i + 1
        return stats


    def most_played_hero(self):
        count = Counter(self.stats["hero"])
        return count.most_common(1)[0][0]


    def get_best_hero(self):
        for hero, stats in self.hero_stats.items():
            if stats["rank"] == 1:
                return hero


    def get_gain_loss(self):
        gain = 0
        wins = 0
        loss = 0
        losses = 0
        for change in self.sr_change:
            if change > 0:
                gain += change
                wins += 1
            elif change < 0:
                loss += change
                losses += 1
        try:
            av_gain = gain / wins
        except ZeroDivisionError:
            av_gain = 0
        try:
            av_loss = loss / losses
        except ZeroDivisionError:
            av_loss = 0
        return (av_gain, av_loss)


    def add_game(self, stats):
        self.open_db()
        command = """
                    INSERT INTO games
                    VALUES (?, ?, ?, ?, ?)"""
        self.crsr.execute(command, stats)
        self.close_db()
