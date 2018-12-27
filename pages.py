import glob
import os
from player import Player


class Page():

    player_names = [os.path.basename(file).replace(".txt", "")
                        for file in glob.glob('./data/players/*.txt')]
    players = []
    for name in player_names:
        players.append(Player(name))

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
            print("Press '%s' for %s" % (p.key.upper(), p.name))
        if self.back != None:
            print("Press 'B' to return to %s" % self.back.name)
        if 'prompt' in dir(self):
            print("Press 'F' to %s" % self.name)
        self.get_page_input()


    def get_page_input(self):
        print()
        #All keys that lead to an option
        options = [key for page in self.to for key in page.key]
        choice  = input().lower()
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
        if name in self.player_names:
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
        pass
