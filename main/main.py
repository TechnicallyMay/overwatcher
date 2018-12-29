import pages


player_page = pages.PlayersPage("Players Menu", "m", "Edit Players")
plot_page = pages.PlotPage("Plot Menu", "p", "View Stats", [player_page])
stat_page = pages.StatPage("Enter Stats Menu", "s", "Enter Stats", [player_page])
main_page = pages.Page("Home", "h", None, [plot_page, stat_page, player_page])


if __name__ == "__main__":
    main_page.show_options()
