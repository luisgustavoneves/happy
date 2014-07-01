# -*- coding: utf-8

LANG = 'english'
wordlist = open('labMTwords-%s.csv' % LANG,'r').read().split('\n')
scores = open('labMTscores-%s.csv' % LANG,'r').read().split('\n')

import re

SPECIAL_CHARS = ['.', ',', '!', '?', '\n']

def get_words(text=''):
    new_text = text
    pos = []
    lastpos = 0
    for char in SPECIAL_CHARS:
        new_text  = new_text.replace(char, ' ')
    new_text = re.sub(' +', ' ', new_text)
    words = new_text.split(' ')

    for word in words:
        lastpos =  text.find(word, lastpos)
        pos.append(lastpos)
        lastpos = lastpos + len(word) -1
    return words, pos

def hi(s, ws=None):

    if not ws:
        s = s.lower()
        s = s.replace('\n', ' ')
        ws, pos = get_words(s)

    df = {}
    for w in ws:
         if w in wordlist and (float(scores[wordlist.index(w)].strip())<=3 or float(scores[wordlist.index(w)].strip())>=7):
            df[w] = df.get(w,0)+1

    h = 0.
    f = 0
    for k in df.keys():
        h = h + df[k]*float(scores[wordlist.index(k)].strip())
        f = f + df[k]

    if f>0:
        return h/f
    else:
        return None

def hgraph(s, window):

    import matplotlib.pyplot as plt

    text = s.lower()
    text = text.replace('\n', ' ')
    ws, pos = get_words(text)

    i = 0
    hs = []

    maxhi = 0
    minhi = 9999999999999999
    maxi = 0
    mini = 0

    while(i+window<=len(ws)):

        #whi = hi('',ws[i:i+window])

        if i>0:
            if ws[i-1] in wordlist and (float(scores[wordlist.index(ws[i-1])].strip())<=3 or float(scores[wordlist.index(ws[i-1])].strip())>=7):
                df[ws[i-1]] = df[ws[i-1]] -1
                if df[ws[i-1]] == 0:
                    df.pop(ws[i-1])
            if ws[i+window-1] in wordlist and (float(scores[wordlist.index(ws[i+window-1])].strip())<=3 or float(scores[wordlist.index(ws[i+window-1])].strip())>=7):
                df[ws[i+window-1]] = df.get(ws[i+window-1],0)+1

        else:

            df = {}
            for w in ws[i:i+window]:
                 if w in wordlist and (float(scores[wordlist.index(w)].strip())<=3 or float(scores[wordlist.index(w)].strip())>=7):
                    df[w] = df.get(w,0)+1

        h = 0.
        f = 0
        for k in df.keys():
            h = h + df[k]*float(scores[wordlist.index(k)].strip())
            f = f + df[k]

        if f>0:
            whi= h/f
        else:
            whi= None

        if whi:
            if whi > maxhi:
                maxhi = whi
                maxi = i
            if whi < minhi:
                minhi= whi
                mini= i
            hs.append(whi)

        i = i + 1

    hs.append(hi('',ws[i:]))

    # this helps figuring out if a small window is meaningful
    print "Max score sequence:", maxhi
    print s[pos[maxi]:pos[maxi+window]+len(ws[maxi+window])]
    print
    print "Min score sequence:", minhi
    print s[pos[mini]:pos[mini+window]+len(ws[mini+window])]

    plt.plot(hs)
    plt.savefig('hgraph.png')


if __name__ == "__main__":

    s1 = '''Shiny Happy People (...)
'''

    s2 = '''Losing My Religion (...)
'''

    s3 = '''Stop Crying Your Heart Out (...)
'''

    s4 = open('prideandprejudice.txt','r').read()


    print hi(s1)
    print hi(s2)
    print hi(s3)
    hgraph(s4,10000) 
