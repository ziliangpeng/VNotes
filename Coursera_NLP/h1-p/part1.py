from sys import stdin
from count_freqs import *

RARE_WORD = '_RARE_'

train_filename = 'gene_replaced_infrequent.train'
input = file(train_filename,"r")

counter = Hmm(3)
counter.train(input)
emission_counts = counter.emission_counts
counter_tag = {}
counter_word = {}
for word, ne_tag in emission_counts:
	if word not in counter_word:
		counter_word[word] = 0
	if ne_tag not in counter_tag:
		counter_tag[ne_tag] = 0
	counter_word[word] += emission_counts[(word, ne_tag)]
	counter_tag[ne_tag] += emission_counts[(word, ne_tag)]

def e(tag, word):
	return float(emission_counts[(word_alias, tag)]) / counter_tag[tag]

#test_filename = 'gene.dev'
#test_filename = 'gene.test'
for line in stdin: #file(test_filename, 'r').readlines():
	line = line.split()
	if len(line) == 0:
		print ''
		continue
	else:
		word = line[0]
	ans = 'None'
	best_emission = -1
	for tag in counter_tag.iterkeys():
		word_alias = word in counter_word and word or RARE_WORD
		emission = e(tag, word_alias)
		if emission > best_emission:
			ans = tag
			best_emission = emission

	print word, ans
