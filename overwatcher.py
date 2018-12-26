from pages import *
from player import Player

# plot_page = PlotPage("Plot", "p", [])
# stat_page = StatPage("Enter Stats", "s", [])
# player_page = PlayersPage("Players Menu", "m", [])
# main_page = Page("Home", "h", [plot_page, stat_page, player_page])
# main_page.show_options()

mason = Player("Mason")

for hero, stats in mason.hero_stats.items():
    print("\n" + hero)
    for key, stat in stats.items():
        print(key, stat, end = " ")
