import glob
import time
import os
from collections import defaultdict
from player import Player


player_names = [os.path.basename(file).replace(".txt", "")
                    for file in glob.glob('./data/players/*.txt')]
players = []
for name in player_names:
    players.append(Player(name))


class Page():

    def __init__(self, name, key, to=[]):
        self.name = name
        #Which key leads to this page
        self.key = key
        #A list of options of where the page can go to
        self.to = to
        #Where the page came from, set by other page objects
        self.back = None


    def show_options(self):
        for p in self.to:
            print("\nPress '%s' for %s" % (p.key.upper(), p.name))
        if self.back != None:
            print("\nPress 'B' to return to %s" % self.back.name)
        if 'prompt' in dir(self):
            print("\nPress 'F' to %s" % self.name)
        self.get_page_input()


    def get_page_input(self):
        #All keys that lead to an option
        options = [key for page in self.to for key in page.key]
        choice  = input("\n").lower()
        if choice == 'b' and self.back != None:
            self.go_back()
        elif choice == 'f' and 'prompt' in dir(self):
            self.prompt()
            self.show_options()
        for i in range(len(options)):
            if choice == options[i]:
                self.to[i].back = self
                self.to[i].show_options()
                self.back = None
                break
        else:
            print('Invalid choice, try again')
            self.show_options()


    def go_back(self):
        self.back.show_options()


class PlotPage(Page):

    def __init__(self, name, key, to=[]):
        super().__init__(name, key, to)


class StatPage(Page):

    def __init__(self,name, key, to=[]):
        super().__init__(name, key, to)


    def prompt(self):
        active_players = [player for player in players if player.active]
        if len(active_players) < 1:
            self.to[0].back = self
            self.to[0].show_options()
        playing = True
        while playing:
            still_playing = input("Would you like to keep entering games? (Y/N) ").lower()
            if still_playing == "n":
                playing = False
                break
            elif still_playing != "y":
                print("Invalid input, try again.")
                self.prompt()

            for player in active_players:
                print("\nEnter stats for %s: " % player.name)
                stats = defaultdict()
                sr_win = self.get_sr(player)
                stats["sr"] = sr_win[0]
                stats["win"] = sr_win[1]
                stats["hero"] = self.get_hero()
                stats["perf"] = self.get_perf()
                stats["time"] = time.strftime("%m %e %y %R").replace(":", " ")
                player.add_game(stats)
                player.activate() #Updates stats for next iteration


    def get_sr(self, player):
        new_sr = int(input("Enter new SR: "))
        sr_change = new_sr - player.stats["sr"][-1]
        if sr_change > 0:
            win = "W"
            print("Nice win! You gained %d SR!" % abs(sr_change))
        elif sr_change == 0:
            win = "T"
            print("Awh a tie! Weird!")
        else:
            win = "L"
            print("Awe shucks, you lost... You lost %d SR..." % abs(sr_change))

        return (new_sr, win)


    def get_hero(self):
        heroes = [line.replace("\n", "") for line in open('data/Heroes.txt')]
        hero = input("Most Played Hero: ")
        if hero in heroes:
            return hero
        else:
            print("Not a real hero! Try again.")
            self.prompt()


    def get_perf(self):
        perf = int(input("Performance 1-10: "))
        if perf <= 10 and perf >= 0:
            return perf
        else:
            print("Out of range, try again")
            self.prompt()


class PlayersPage(Page):

    def __init__(self,name, key, to=[]):
        super().__init__(name, key, to)


    def prompt(self):
        choice = input("Would you like to add players (A), or set active players (S)?").lower()
        if choice == "a":
            self.add_player()
        elif choice == "s":
            self.set_active()
        else:
            print("Invalid choice, going back.")
            self.go_back()


    def add_player(self):
        name = input("Please enter player's name: ")
        if name in player_names:
            print("Player already exists, try again.")
            self.add_player()
        sr = input("Please enter player's starting SR: ")
        try:
            sr = int(sr)
        except ValueError:
            print("Invalid input, try again.")
            self.add_player()
        player = Player(name, sr)



    def set_active(self):
        print("Which players would you like to activate?")
        for i in range(len(players)):
            print(i + 1, players[i].name)
        choices = input().split()
        print()
        active = []
        for choice in choices:
            player = players[int(choice) - 1]
            player.activate()
            active.append(player)
            print(player.name + " is now active!")
        print()
        for player in players:
            if player not in active:
                player.deactivate()
