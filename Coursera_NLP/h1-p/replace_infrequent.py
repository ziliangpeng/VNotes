
""" read 'y x' list from stdin, replace infrequent words(cnt < 5) and print new
    list to stdout
"""

RARE_WORD = '_RARE_'
INFREQUENT_THRESHOLD = 5

seq = []
cnt = {}
while True:
    try:
        a = raw_input()
    except EOFError:
        break
    a = a.split()
    if len(a) == 0:
        seq.append('EOF')
    else:
        word = a[0]
        tag = a[1]
        seq.append((word, tag))
        if word not in cnt:
            cnt[word] = 0
        cnt[word] += 1

for item in seq:
    if item == 'EOF':
        print ''
    else:
        word = item[0]
        tag = item[1]
        if cnt[word] < INFREQUENT_THRESHOLD:
            word = RARE_WORD
        print word, tag
