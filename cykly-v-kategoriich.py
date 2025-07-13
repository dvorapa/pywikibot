import pywikibot

# s site
s = pywikibot.Site()

# a set pismen
a = set()
# v set kategorii v cyklu
v = set()
# w list potencialnich kategorii jednotlivych cyklu
w = []
# i kategorie
for i in s.allpages(namespace=14):
    # m generator podkategorii
    m = i.subcategories(recurse=True)
    if next(m, False) and next(i.categories().__iter__(), False):
        # b pismeno
        b = i.title(with_ns=False)[0]
        if not b in a:
            a.add(b)
            print(b, flush=True)
        # g list potencialnich kategorii cyklu
        g = []
        # f set videnych podkategorii
        f = set()
        # j podkategorie
        for j in m:
            if g:
                g.append(j)
            elif j in f:
                break
            if j == i:
                v.add(i)
                if not g:
                    g.append(i)
                else:
                    w.append(g)
                    g.clear()
                    print(i, flush=True)
                    break
            f.add(j)


# f set videnych cyklu
f = set()
f.add(frozenset(pywikibot.Category(s, 'Kategorie:Wikipedie:Neindexované stránky')))
# t list stringu jednotlivych cyklu
t = []
# g list potencialnich kategorii cyklu
for g in w:
    # l list kategorii cyklu
    l = []
    # i potencialni kategorie cyklu
    for i in g:
        if i in v:
            l.append(i)
    # u set kategorii cyklu
    u = frozenset(l)
    if not u in f:
        f.add(u)
        t.append(' > '.join(i.title(as_link=True, textlink=True) for i in l))

# p page
p = pywikibot.Page(s, 'Wikipedie:Údržbové seznamy/Cykly v kategoriích/seznam')
p.text += '\n# ' + '\n# '.join(t)
p.save(summary='Robot: aktualizace')
