#!/usr/bin/env python3
import pywikibot

s = pywikibot.Site()

f = set()  # set of seen looping cats
a = ''
t = set()
for i in s.allpages(namespace=14):
  # is a subcategory and contains 1 or more subcategories and hasn't been seen yet
  if not i.isEmptyCategory() and next(i.categories(total=1), False) and not i in f:
    b = i.title(with_ns=False)[0]
    if b != a:  # print first letter for progress
      a = b
      print(b)
    del(b)
    c = i.subcategories(recurse=True)
    if i in c:  # is there a loop?
      g = []  # list of current looping cats
      d = g.append
      for j in c:
        if g:  # add loop member
          d(j)
        if j == i:  # found beginning/end of the loop
          if not g:  # start tracking the loop
            d(i)
          else:  # finish loop
            t.add('\n# ' + ' > '.join(k.title(as_link=True, textlink=True) for k in g))
            f.update(g)
            print(g)
            del(d)
            del(g)
            break

p = pywikibot.Page(s, 'Wikipedie:Údržbové seznamy/Cykly v kategoriích/seznam')
p.text += ''.join(t)
p.save(summary='Robot: aktualizace')
