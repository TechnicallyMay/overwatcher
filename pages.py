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

    def __init__(self, name, key, description, to=[]):
        self.name = name
        #Which key leads to this page
        self.key = key
        #A list of options of where the page can go to
        self.to = to
        #Where the page came from, set by other page objects
        self.back = None
        self.description = description


    def show_options(self):
        print(self.get_header())
        for p in self.to:
            print("Press '%s' for %s" % (p.key.upper(), p.name))
        if self.back != None:
            print("Press 'B' to return to %s" % self.back.name)
        if 'prompt' in dir(self):
            print("Press 'F' to %s" % self.description)
        self.get_page_input()


    def get_header(self):
        max_length = 25
        name_length = len(self.name)
        buffer = max_length - name_length
        side = "=" * round(buffer / 2)
        header = side + self.name.upper() + side

        return header


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

    def __init__(self, name, key, description, to=[]):
        super().__init__(name, key, description, to)


class StatPage(Page):

    def __init__(self, name, key, description, to=[]):
        super().__init__(name, key, description, to)


    def prompt(self):
        active_players = [player for player in players if player.active]
        if len(active_players) < 1:
            print("Please select active players.\n")
            self.to[0].back = self
            self.to[0].show_options()
        playing = True
        while playing:
            still_playing = input("Would you like to enter games? (Y/N) ").lower()
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
        valid = False
        while not valid:
            new_sr = input("Enter new SR: ")
            try:
                int_sr = int(new_sr)
                valid = True
            except ValueError:
                print("\nInvalid input, try again")

        sr_change = int_sr - player.stats["sr"][-1]
        if sr_change > 0:
            win = "W"
            print("Nice win! You gained %d SR!" % abs(sr_change))
        elif sr_change == 0:
            win = "T"
            print("Awh a tie! Weird!")
        else:
            win = "L"
            print("Awe shucks, you lost... You lost %d SR..." % abs(sr_change))

        return (int_sr, win)


    def get_hero(self):
        valid = False
        heroes = [line.replace("\n", "") for line in open('data/Heroes.txt')]
        while not valid:
            hero = input("Most Played Hero: ")
            if hero in heroes:
                valid = True
            else:
                print("\nNot a real hero! Try again.")

        return hero


    def get_perf(self):
        valid = False
        while not valid:
            perf = input("Performance 1-10: ")
            try:
                int_perf = int(perf)
                if int_perf <= 10 and int_perf >= 0:
                    valid = True
                else:
                    print("Out of range, try again")
            except ValueError:
                print("\nInvalid input, try again")

        return int_perf


class PlayersPage(Page):

    def __init__(self, name, key, description, to=[]):
        super().__init__(name, key, description, to)


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
        players.append(Player(name, sr))



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
