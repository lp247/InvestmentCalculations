from matplotlib import pyplot as plt


class PlotSeries:
    def __init__(self, label: str):
        self.label = label
        self.values = []

    def put_value(self, value: int):
        self.values.append(value)


def plot(data: dict):
    # Assume all have the same length
    lengthOfTime = len(data["series"][0].values)
    for series in data["series"]:
        values = series.values
        label = series.label
        plt.plot(
            list(range(len(values))),
            values,
            label=label,
        )
    plt.title(data["title"])
    plt.xlabel(data["xlabel"])
    plt.ylabel(data["ylabel"])
    plt.gca().set_xticks([i for i in range(0, lengthOfTime + 1, 120)])
    plt.gca().set_xticklabels([str(i // 12) for i in range(0, lengthOfTime + 1, 120)])
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()
