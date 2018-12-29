import pages


plot_page = pages.PlotPage("Plot", "p", "View Charts")
player_page = pages.PlayersPage("Players Menu", "m", "Edit Players")
stat_page = pages.StatPage("Enter Stats", "s", "Enter Stats", [player_page])
main_page = pages.Page("Home", "h", None, [plot_page, stat_page, player_page])
main_page.show_options()


# for hero, stats in mason.hero_stats.items():
#     print("\n" + hero)
#     for key, stat in stats.items():
#         print(key, stat, end = " ")
