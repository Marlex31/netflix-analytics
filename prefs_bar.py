import json
from collections import Counter, OrderedDict
from matplotlib import pyplot as plt


with open("db.json", "r", encoding="utf-8") as f:
    json_db = json.loads(f.read())

genres = []
for item in json_db.values():
    for i in item[1]:
        genres.append(i)


genres = dict(Counter(genres))
genres = dict(OrderedDict(sorted(genres.items())))
# name, genre = list(zip(*genres.items()))

plt.title("Genre preference across all watched media")
plt.xlabel("Genres")
plt.ylabel("Amount watched")
plt.tight_layout()

# plt.bar(
#     [x for x in range(len(genres))],
#     height=genres.values(),
#     tick_label=["heya" for x in range(len(genres))],
# )
# plt.tick_params(axis="both", which="major", labelsize=1)

plt.bar(x=genres.keys(), height=genres.values())
plt.show()
