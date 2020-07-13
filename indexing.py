import re
import csv

from sklearn.feature_extraction.text import CountVectorizer


def reader(file, index=0): 
 
	with open(file, 'r', encoding="utf8") as f:
		f_read = csv.reader(f) 
		next(f_read)

		for line in f_read:
			yield line[index]

for line in reader('sample.csv'):
	print(line)

# cv = CountVectorizer(lowercase=False)
# cv_fit = cv.fit_transform(reader('sample.csv'))

# names = cv.get_feature_names()
# ranking_list = cv_fit.toarray().sum(axis=0).tolist()
# ranking = dict(zip(names, ranking_list))

# print(ranking)