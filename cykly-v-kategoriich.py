from pywikibot import Site, Category, Page
from tarjan import tarjan
from networkx import DiGraph, simple_cycles

# s site
s = Site()
# a pocet proslych kategorii
a = 0
# m dict primych podkategorii
m = {}
# v list silne souvislych komponent s cyklem
v = []
# c prochazena kategorie
for c in s.allpages(namespace=14):
    if not a % 7000:
        print(c.title(with_ns=False)[:2], flush=True)
    a += 1
    m[c] = list(c.subcategories(recurse=1))
    if c in m[c]:
        print(c, flush=True)
        v.append([c])
print(str(a) + ' read categories')

# t list silne souvislych komponent
for t in tarjan(m):
    if len(t) > 1:
        print(t, flush=True)
        v.append(t)

# j vyjimka
j = [Category(s, 'Kategorie:Wikipedie:Neindexované stránky')]
if j in v:
    v.remove(j)

if v:
    v.sort(key=len)
    # l list stringu objevenych cyklu
    l = []
    # o silne souvisla komponenta
    for o in v:
        if len(o) > 2:
            # z dict primych podkategorii
            z = {}
            # u kategorie v silne souvisle komponente
            for u in o:
                z[u] = list(u.subcategories(recurse=1))
            # w jednotlivy cyklus
            for w in simple_cycles(DiGraph(z)):
                l.append(' > '.join(g.title(as_link=True, textlink=True) for g in w + [w[0]]))
        else:
            l.append(' > '.join(g.title(as_link=True, textlink=True) for g in o + [o[0]]))

    # p page
    p = Page(s, 'Wikipedie:Údržbové seznamy/Cykly v kategoriích/seznam')
    p.text = '\n# ' + '\n# '.join(l)
    p.save(summary='Robot: aktualizace')
