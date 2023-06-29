import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def analyze(productcode):
    opinions = pd.read_json(f"app/static/opinions/{productcode}.json")

    max_score = 5

    opinions['stars'] = (opinions['score']*max_score).round(1)

    opinions_count = opinions.shape[0]
    pros_count = opinions.pros.astype(bool).sum()
    cons_count = opinions.cons.astype(bool).sum()
    average_score = (opinions.stars.mean()).round(2)

    recommendations = opinions.recommendation.value_counts(dropna=False).reindex([True, False, np.nan], fill_value=0)
    recommendations.plot.pie(
        label="",
        labels = ["Recommend", "Not recommend", "Neutral"],
        colors = ["forestgreen", "crimson", "gray"],
        autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else ''
        )
    plt.title("Recommandations")
    plt.savefig(f"app/static/charts/{productcode}_pie.png")
    plt.close()

    stars = opinions.stars.value_counts().reindex(list(np.arange(0, 5.5, 0.5)), fill_value=0)
    stars.plot.bar()
    plt.ylim(0, max(stars)+10)
    plt.title("Star count distribution")
    plt.xlabel("Number of stars")
    plt.ylabel("Number of opinions")
    plt.xticks(rotation = 0)
    plt.grid(True, "major", "y")
    for index, value in enumerate(stars):
        plt.text(index, value+1.5, str(value), ha = "center")
    plt.savefig(f"app/static/charts/{productcode}_bar.png")

    return [average_score, opinions_count, pros_count, cons_count]
