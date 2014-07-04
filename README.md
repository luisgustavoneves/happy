happy
=====

Happiness meter for python. A sentiment analysis tool based on papers:

http://www.uvm.edu/storylab/share/papers/dodds2014a/index.html

http://www.uvm.edu/~cdanfort/research/dodds-danforth-johs-2009.pdf

Setup
-----

First download files for target language:

http://www.uvm.edu/storylab/share/papers/dodds2014a/data.html

Then configure your language at the beginning of the code:

```python
LANG = "target_language"
```

Usage
-----

```python
import happy as h
# shows text overall happiness index. Scale 1 (sad) to 9 (happy). Lower and upper limits for word filtering are optional,
# default is 3 and 7 (only words with score bellow 3 or over 7 are considered).
print h.hi(text, 4, 6)
# make an html page with point and click happiness graph with specified window. Lower and upper limits also configurable, 
# window, lower and upper are optional. 
h.hgraph('title', text, window, l, u)
```

Requirements
------------

- python 2.7
- flot (for happiness graph) already included in source.
