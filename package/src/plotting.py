from typing import List, TypedDict
from matplotlib import pyplot as plt


class PlotSeries:
    def __init__(self, label: str):
        self.label = label
        self.values: List[float] = []

    def put_value(self, value: float):
        self.values.append(value)


class Data(TypedDict):
    series: List[PlotSeries]
    title: str
    xlabel: str
    ylabel: str
    legend_loc: str
    yscale: str


def plot(data: Data):
    # Assume all have the same length
    lengthOfTime = len(data["series"][0].values)
    for series in data["series"]:
        values = series.values
        label = series.label
        plt.plot(  # type: ignore
            list(range(len(values))),
            values,
            label=label,
        )
    plt.title(data["title"])  # type: ignore
    plt.xlabel(data["xlabel"])  # type: ignore
    plt.ylabel(data["ylabel"])  # type: ignore
    plt.gca().set_xticks([i for i in range(0, lengthOfTime + 1, 120)])  # type: ignore
    plt.gca().set_xticklabels([str(i // 12) for i in range(0, lengthOfTime + 1, 120)])  # type: ignore
    plt.yscale(data["yscale"])  # type: ignore
    plt.legend(loc=data["legend_loc"])  # type: ignore
    plt.grid(True)  # type: ignore
    plt.show()  # type: ignore
