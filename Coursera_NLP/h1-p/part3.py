from sys import stdin
from count_freqs import *
from collections import defaultdict
import string
from rare import *

START_TAG = '*'
STOP_TAG = 'STOP'
train_filename = 'gene_grouped_rare.train'
input = file(train_filename, "r")

counter = Hmm(3)
counter.train(input)
emission_counts = counter.emission_counts
trigram_counts = counter.ngram_counts[2]
bigram_counts = counter.ngram_counts[1]
unigram_counts = counter.ngram_counts[0]

counter_tag = defaultdict(int)
counter_word = defaultdict(int)
for word, ne_tag in emission_counts:
	counter_word[word] += emission_counts[(word, ne_tag)]
	counter_tag[ne_tag] += emission_counts[(word, ne_tag)]

def alias(word):
	if word in counter_word:
		return word
	else:
		return group(word)

def e(tag, word):
	return float(emission_counts[(alias(word), tag)]) / counter_tag[tag]

def q(y0, y1, y2):
	return float(trigram_counts[(y0, y1, y2)]) / bigram_counts[(y0, y1)]

def viterbi(words):
	length = len(words)

	dp = [defaultdict(int) for i in range(length)]
	back = [defaultdict(int) for i in range(length)]

	# initial
	for tag in counter_tag.iterkeys():
		word = alias(words[0])
		dp[0][(START_TAG, tag)] = q(START_TAG, START_TAG, tag) * e(tag, word)
		back[0][(START_TAG, tag)] = START_TAG

	# dp
	for k in range(1, length):
		for tag in counter_tag.iterkeys():
			word = alias(words[k])
			for w, u in dp[k-1].iterkeys():
				if w == STOP_TAG or u == STOP_TAG:
					continue
				value = dp[k-1][(w, u)] * q(w, u, tag) * e(tag, word)
				if value >= dp[k][(u, tag)]:
					dp[k][(u, tag)] = value
					back[k][(u, tag)] = w

	total = -1
	chosen = None
	for w, u in dp[length-1].iterkeys():
		value = dp[length-1][(w, u)] * q(w, u, STOP_TAG)
		if value >= total:
			total = value
			chosen = (w, u)

	result_tags = list(reversed(chosen))
	for k in range(length-1, 0, -1):
		prev = back[k][chosen]
		result_tags.append(prev)
		chosen = (prev, chosen[0])

	return reversed(result_tags[:length])


words = []
for line in map(string.split, stdin):
	if len(line) == 0:
		for word, tag in zip(words, viterbi(words)):
			print word, tag
		print ''
		words = []
	else:
		word = line[0]
		words.append(word)

if words:
	for word, tag in zip(words, viterbi(words)):
		print word, tag
