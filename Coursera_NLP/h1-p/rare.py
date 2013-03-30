

NUMERIC = '_NUM_'
ALL_CAP = '_ALL_CAPS_'
LAST_CAP = '_LAST_CAP_'
RARE_WORD = '_RARE_'
INFREQUENT_THRESHOLD = 5


def group(word):
	if set(word) & set('1234567890'):
	    word = NUMERIC
	elif set(word) - set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') == set():
	    word = ALL_CAP
	elif word[-1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
	    word = LAST_CAP
	else:
	    word = RARE_WORD
	return word

def rare(word):
	return RARE_WORD