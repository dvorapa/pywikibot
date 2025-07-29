from pywikibot import Site, Category, Page
from networkx import DiGraph, simple_cycles

# s site
s = Site()
# a pocet proslych kategorii
a = 0
# m dict primych podkategorii
m = {}
# c prochazena kategorie
for c in s.allpages(namespace=14):
    if not a % 7000:
        print(c.title(with_ns=False)[:2], flush=True)
    a += 1
    m[c] = list(c.subcategories(recurse=1))
print(str(a) + ' read categories')

# v list objevenych cyklu
v = sorted(simple_cycles(DiGraph(m)), key=len)

# j vyjimka
j = [Category(s, 'Kategorie:Wikipedie:Neindexované stránky')]
if j in v:
    v.remove(j)

if v:
    # l list stringu jednotlivych cyklu
    l = []
    # o cyklus
    for o in v:
        print(o, flush=True)
        # g kategorie jednoho cyklu
        l.append(' > '.join(g.title(as_link=True, textlink=True) for g in o + [o[0]]))

    # p page
    p = Page(s, 'Wikipedie:Údržbové seznamy/Cykly v kategoriích/seznam')
    p.text = '\n# ' + '\n# '.join(l)
    p.save(summary='Robot: aktualizace')
