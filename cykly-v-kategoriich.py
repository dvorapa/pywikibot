from pywikibot import Site, Category, Page
from tarjan import tarjan

# s site
s = Site()
# a pocet proslych kategorii
a = 0
# m dict primych podkategorii
m = {}
# v list objevenych cyklu
v = []
# c prochazena kategorie
for c in s.allpages(namespace=14):
    if not a % 7000:
        print(c.title(with_ns=False)[:2], flush=True)
    a += 1
    m[c] = list(c.subcategories(recurse=1))
    if c in m[c]:
        print(c, flush=True)
        v.append([c] * 2)
print(str(a) + ' read categories')

# t list potencialniho cyklu
for t in tarjan(m):
    if len(t) > 1:
        print(t, flush=True)
        v.append(t + [t[0]])

# j vyjimka
j = [Category(s, 'Kategorie:Wikipedie:Neindexované stránky')] * 2
if j in v:
    v.remove(j)

if v:
    # l list stringu jednotlivych cyklu
    l = []
    # o silne souvisla komponenta
    for o in v:
        if len(o) > 3:
            # z cyklus
            z = []
            # q kategorie v ssk
            q = o[0]
            z.append(q)
            o.remove(q)
            while o:
                q = [n for n in q.subcategories(recurse=1) if n in o][0]
                z.append(q)
                o.remove(q)
            o = z
        l.append(' > '.join(g.title(as_link=True, textlink=True) for g in o))

    # p page
    p = Page(s, 'Wikipedie:Údržbové seznamy/Cykly v kategoriích/seznam')
    p.text = '\n# ' + '\n# '.join(l)
    p.save(summary='Robot: aktualizace')
