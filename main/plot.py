import matplotlib.pyplot as plt


class Plot():

    def __init__(self, data, title):
        self.data = data
        self.title = title


    def show(self):
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.legend()
        plt.show()


class SRPlot(Plot):

    def __init__(self, data, title, players):
        super().__init__(data, title)
        self.xlabel = "Game"
        self.ylabel = "SR"
        self.players = players
        self.get_lims()


    def get_lims(self):
        all_sr_values = [sr for list in self.data for sr in list]
        max_sr = max(all_sr_values)
        min_sr = min(all_sr_values)
        longest = max([len(list) for list in self.data])
        self.y_lim = (min_sr - 500, max_sr + 500)
        self.x_lim = (0, longest + 2)


    def build(self):
        fig, ax = plt.subplots()
        for i, set in enumerate(self.data):
            ax.plot(range(len(set)),
                    set,
                    label = self.players[i].name,
                    marker = ".")
        ax.set(xlabel = self.xlabel, ylabel = self.ylabel,
               title = self.title)
        y_ticks = [0, 1500, 2000, 2500, 3000, 3500, 4000]
        ax.set_yticks(y_ticks)
        self.fill_rank_colors(y_ticks)
        plt.xlim(self.x_lim)
        plt.ylim(self.y_lim)


    def fill_rank_colors(self, start_ys):
        rank_colors = ["#cd7f32", "#D3D3D3", "#DAA520",
                       "#A0AABF", "#9ac5db", "#ff80ff",
                       "#ff8080"]
        x_vals = [i for i in range(self.x_lim[1] + 5)]
        for i in range(len(start_ys)):
            y1_vals = [start_ys[i]] * len(x_vals)
            try:
                y2_vals = [start_ys[i + 1]] * len(x_vals)
            except IndexError:
                y2_vals = [5000] * len(x_vals)
            plt.fill_between(x_vals, y1_vals,
                            y2_vals, color = rank_colors[i],
                             alpha = .4)


class SRByHero(Plot):

    def __init__(self, data, title):
        super().__init__(data, title)
        self.xlabel = "Hero"
        self.ylabel = "Average Change in SR"


class WinLossByHero(Plot):

    def __init__(self, data, title):
        super().__init__(data, title)
        self.xlabel = "Hero"
        self.ylabel = "Win / Loss Ratio"


class PerformancePlot(Plot):

    def __init__(self, data, title):
        super().__init__(data, title)
        self.xlabel = "Change in SR"
        self.ylabel = "Performance"
        self.players = players
