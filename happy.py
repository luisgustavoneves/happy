# -*- coding: utf-8

LANG = 'english'
wordlist = open('labMTwords-%s.csv' % LANG,'r').read().split('\n')
scores = open('labMTscores-%s.csv' % LANG,'r').read().split('\n')

html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <script language="javascript" type="text/javascript" src="%s_FILES/jquery.js"></script>
    <script language="javascript" type="text/javascript" src="%s_FILES/jquery.flot.js"></script>
    <script language="javascript" type="text/javascript" src="%s_FILES/jquery.flot.axislabels.js"></script>
</head>
<body>
<h1> Happiness Index Sliding Window</h1>
<h3> %s </h3>
<br>
<p> Click on the series to show the related window</p>

<div id="flot" style="width:800px;height:347px;">
</div>
<br>
<div id="window" style="width:800px;height:400px;padding:20px;white-space: pre-wrap;overflow-y:auto">
<br>
<div id="text" style="display:none;">%s</div>
</body>
    <script type="text/javascript">
    
    $(function() {

        var text = $('#text').html();
        $("#window").text(text);
        $("#window").scrollTop(0);

        var w = %d;
        var hs = %s;
        var hspos = %s;
        var d1 = [];
        for (var i = 0; i < hs.length; i ++) {
                d1.push([i, hs[i]]);
            }

        var plot = $.plot("#flot", [d1],{ xaxes: [{axisLabel: 'Window Position (in words)'}],yaxes: [{axisLabel: 'Happiness or Positivity'}],grid: {clickable: true, "hoverable" : true}});


        $("#flot").bind("plotclick", function (event, pos, item) {

            if (item) {
                plot.unhighlight();
                plot.highlight(item.series, item.datapoint);
                var i = item.dataIndex;
                if (i+w<hspos.length) {
                    $("#window").text(text.slice(hspos[i], hspos[item.dataIndex + w]));
                }
                else {
                    $("#window").text(text.slice(hspos[i]));
                }
                $("#window").scrollTop(0);
            }
        });


    });
    </script>

</html>
'''

import re
import shutil, os

SPECIAL_CHARS = ['.', ',', '!', '?', '\n']

def get_words(text=''):
    new_text = text
    pos = []
    lastpos = 0
    for char in SPECIAL_CHARS:
        new_text  = new_text.replace(char, ' ')
    new_text = re.sub(' +', ' ', new_text)
    words = []

    for word in new_text.split(' '):
        if word:
            lastpos =  text.find(word, lastpos)
            pos.append(lastpos)
            words.append(word)
            lastpos = lastpos + len(word) -1
    return words, pos

def hi(s,l=3, u=7):

    s = s.lower()
    s = s.replace('\n', ' ')
    ws, pos = get_words(s)
    
    worddic = {} # dic with words in selected range and their scores
    for i, word in enumerate(wordlist):
        word_score = float(scores[i].strip())
        if word_score<=l or word_score>=u:
            worddic[word] = word_score

    h = 0. #sum of happiness scores
    f = 0   #sum of word freq.

    df = {} #dic with word frequency in text
    for w in ws:
         if w in worddic.keys():
            df[w] = df.get(w,0)+1
            h = h + worddic[w]
            f = f +1

    if f>0:
        return h/f
    else:
        return None # no word found in wordlist, maybe l and u too restrictive

def hgraph(title,s, window=10000,l=3, u=7):

    shutil.rmtree(title+'_FILES', True)
    os.mkdir(title+'_FILES')
    shutil.copy('jquery.js', title+'_FILES')
    shutil.copy('jquery.flot.js', title+'_FILES')
    shutil.copy('jquery.flot.axislabels.js', title+'_FILES')

    text = s.lower()
    text = text.replace('\n', ' ')
    ws, pos = get_words(text)

    worddic = {} # dic with words in selected range and their scores
    for i, word in enumerate(wordlist):
        word_score = float(scores[i].strip())
        if word_score<=l or word_score>=u:
            worddic[word] = word_score

    i = 0
    hs = []
    hspos = []

    maxhi = 0
    minhi = 9999999999999999
    maxi = 0
    mini = 0

    while(i+window<=len(ws)):


        if i>0: # for the other windows just remove the first word in the last window add the new word at the end of new window
            if ws[i-1] in worddic.keys():
                df[ws[i-1]] = df[ws[i-1]] -1
                h = h - worddic[ws[i-1]]
                f = f -1
                if df[ws[i-1]] == 0:
                    df.pop(ws[i-1])
            if ws[i+window-1] in worddic.keys():
                df[ws[i+window-1]] = df.get(ws[i+window-1],0)+1
                h = h + worddic[ws[i+window-1]]
                f = f + 1
        else: # for the first window it is just like hi()
            h = 0.
            f = 0
            df = {}
            for w in ws[i:i+window]:
                 if w in worddic.keys():
                    df[w] = df.get(w,0)+1
                    h = h + worddic[w]
                    f = f +1

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
            hspos.append(pos[i])

        i = i + 1

    # this helps figuring out if a small window is meaningful
    print "Max score sequence:", maxhi
    print s[pos[maxi]:pos[maxi+window]+len(ws[maxi+window])]
    print
    print "Min score sequence:", minhi
    print s[pos[mini]:pos[mini+window]+len(ws[mini+window])]

    arq_html = open(title+'.html', 'w')
    arq_html.write(html%(title, title, title, title, s, window,str(hs), str(hspos)))

if __name__ == "__main__":

    s1 = '''
Shiny Happy People (...)
'''

    s2 = '''
Losing My Religion (...)
'''

    s3 = '''
Stop Crying Your Heart Out (...)
'''

    s4 = open('prideandprejudice.txt','r').read()

    print hi(s1)
    print hi(s2)
    print hi(s3)
    hgraph('Pride and Prejudice', s4)
