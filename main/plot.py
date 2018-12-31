import matplotlib.pyplot as plt


class Plot():

    def __init__(self, title):
        self.title = title
        fig, self.ax = plt.subplots()


    def show(self):
        self.set_axis_labels()
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.show()


    def set_axis_labels(self):
        if "x_lim" in dir(self):
            plt.xlim(self.x_lim)
        if "y_lim" in dir(self):
            plt.ylim(self.y_lim)
        if "x_ticks" in dir(self):
            self.ax.set_xticks(self.x_ticks)
        if "x_labels" in dir(self):
            self.ax.set_xticklabels(self.x_labels, rotation = 90)
        if "y_ticks" in dir(self):
            self.ax.set_yticks(self.y_ticks)
        if "y_labels" in dir(self):
            self.ax.set_yticklabels(self.y_labels)


class SRPlot(Plot):

    def __init__(self, title):
        super().__init__(title)
        self.xlabel = "Game"
        self.ylabel = "SR"
        self.x_lim = (0, 0)
        self.y_lim = (7000, 0)
        self.y_ticks = [0, 1500, 2000, 2500, 3000, 3500, 4000]


    def check_limits(self, data):
        data_lim_top = max(data) + 500
        data_lim_bottom = min(data) - 500
        if data_lim_top > self.y_lim[1]:
            self.y_lim = (self.y_lim[0], data_lim_top)
        if data_lim_bottom < self.y_lim[0]:
            self.y_lim = (data_lim_bottom, self.y_lim[1])
        if len(data) > self.x_lim[1]:
            self.x_lim = (0, len(data) + 2)


    def add(self, data, name):
        self.ax.plot(range(len(data)),
                     data,
                     label = name,
                     marker = "."
                     )
        self.check_limits(data)


    def build(self):
        self.fill_rank_colors()
        plt.legend()


    def fill_rank_colors(self):
        rank_colors = ["#cd7f32", "#D3D3D3", "#DAA520",
                       "#A0AABF", "#9ac5db", "#ff80ff",
                       "#ff8080"]
        x_vals = range(self.x_lim[1] + 5)
        for i in range(len(self.y_ticks)):
            y1_vals = [self.y_ticks[i]] * len(x_vals)
            try:
                y2_vals = [self.y_ticks[i + 1]] * len(x_vals)
            except IndexError:
                y2_vals = [5000] * len(x_vals)
            plt.fill_between(x_vals, y1_vals, y2_vals,
                             color = rank_colors[i],
                             alpha = .4)


class WinLossByHero(Plot):

    def __init__(self, title):
        super().__init__(title)
        self.xlabel = "Hero"
        self.ylabel = "Win / Loss Ratio"
        self.y_lim = (0, 1)
        self.win_bars = []
        self.loss_bars = []
        self.x_labels = []


    def add(self, win_loss, hero):
        self.win_bars.append(win_loss)
        self.loss_bars.append(1 - win_loss)
        self.x_labels.append(hero)


    def build(self):
        num_of_bars = range(len(self.win_bars))
        self.x_ticks = num_of_bars
        self.ax.bar(num_of_bars, self.win_bars, color = "green")
        self.ax.bar(num_of_bars, self.loss_bars, color = "red",
                    bottom = self.win_bars)


class SRByHero(Plot):

    def __init__(self, title):
        super().__init__(title)
        self.xlabel = "Hero"
        self.ylabel = "Average Change in SR"
        self.bars = []
        self.x_labels = []
        self.x_ticks = []


    def add(self, change, hero):
        self.bars.append(change)
        self.x_labels.append(hero)


    def build(self):
        num_of_bars = range(len(self.bars))
        self.x_ticks = num_of_bars
        self.ax.bar(num_of_bars, self.bars, width = 1,
                    edgecolor = "black")
        plt.grid(axis = "y", alpha = 0.5)


class PerformancePlot(Plot):

    def __init__(self, title):
        super().__init__(title)
        self.xlabel = "Change in SR"
        self.ylabel = "Performance"
        self.xlim = (-30, 30)
        self.ylim = (-1, 11)
        self.x_ticks = range(-30, 35, 10)
        self.x_labels = ["-30", "-20", "-10", "0", "+10", "+20", "+30"]
        self.y_ticks = range(11)


    def add(self, change, performance, name):
        self.ax.scatter(change,
                        performance,
                        label = name,
                        )


    def build(self):
        plt.legend()
