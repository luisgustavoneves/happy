happy
=====

Happiness meter for python. A sentiment analisys tool based on papers:

http://www.uvm.edu/storylab/share/papers/dodds2014a/index.html

http://www.uvm.edu/~cdanfort/research/dodds-danforth-johs-2009.pdf

Setup
-----

First download files for target language:

http://www.uvm.edu/storylab/share/papers/dodds2014a/data.html

Then configure your language at the begining of the code:

```python
LANG = "target_language"
```

Usage
-----

```python
import happy as h
# shows text overall happiness index. Scale 1 (sad) to 9 (happy)
print h.hi(text)
# display text happiness graph for specified window. Also displays text slices with max and min scores.
h.hgraph(text, 10000)
```
