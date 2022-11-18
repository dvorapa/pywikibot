#!/usr/bin/env python3
import pywikibot

s = pywikibot.Site()

f = set()  # set of seen looping cats
a = ''
t = ''
for i in s.allpages(namespace=14):
  # is a subcategory and contains 1 or more subcategories and hasn't been seen yet
  if not i.isEmptyCategory() and next(i.categories(total=1), False) and not i in f:
    b = i.title(with_ns=False)[0]
    if b != a:  # print first letter for progress
      a = b
      print(b)
    c = i.subcategories(recurse=True)
    if i in c:  # is there a loop?
      g = set()  # set of current looping cats
      for j in c:
        if g:  # add loop member
          g.add(j)
        if j == i:  # found beginning/end of the loop
          if not g:  # start tracking the loop
            g.add(i)
          else:  # finish loop
            t += '\n# ' + ' > '.join(k.title(as_link=True, textlink=True) for k in g)
            f.update(g)
            print(g)
            g = set()
            break

p = pywikibot.Page(s, 'Wikipedie:Údržbové seznamy/Cykly v kategoriích/seznam')
p.text += t
p.save(summary='Robot: aktualizace')
