import json
import csv
from collections import Counter
import datetime

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from utillities import convert_time


with open('db.json', 'r', encoding='utf-8') as f:
    json_db = json.loads(f.read())

with open('netflix.csv', 'r', encoding="utf8") as f:
    f_read = csv.reader(f)
    next(f_read)
    csv_db = [line for line in f_read]

titles_counter = {}
for item in json_db.keys():
    for title in csv_db:
        if title[0].startswith(item):
            if item not in titles_counter.keys():
                titles_counter.update({item: []})
            titles_counter[item].append(title[1])

for i, j in titles_counter.items():
    titles_counter[i] = dict(Counter(j))


activity = {}
for i in titles_counter.items():
    for j, k in i[1].items():
        date = j.split('/')
        year = '20' + date[-1]
        if year not in activity.keys():
            activity.update({year: [{x: [0 for y in range(7)]} for x in range(12)]})

        date = list(map(int, date))
        date.reverse()
        dummy_date = date.copy()
        date = dummy_date[0], dummy_date[2], dummy_date[1]  # find another way to change date format
        week_day = datetime.date(*date).weekday()
        month = datetime.date(*date).month - 1

        activity[year][month][month][week_day] += json_db[i[0]][2] * k


test_data = []
for mon in activity['2019']:
    for i in mon.values():
        for j in i:
            test_data.append(round(j, 2))

formatted_data = []
for x in range(0, 84, 7):
    formatted_data.append(test_data[x:x+7])

data = np.array(formatted_data)
data = np.fliplr(np.rot90(data, k=3))
data = np.absolute(data)

day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
               'Aug', 'Sep', 'Oct', 'Dec', 'Nov']


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


fig, ax = plt.subplots()
im, cbar = heatmap(data, day_names, month_names, ax=ax,
                   cmap="YlGn", cbarlabel="Monthly hours of watchtime")
texts = annotate_heatmap(im, valfmt="{x}")

fig.tight_layout()
plt.show()
