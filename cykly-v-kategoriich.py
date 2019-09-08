import pywikibot

s = pywikibot.Site()

a = set()
v = set()
w = []
for i in s.allpages(namespace=14):
    b = i.title(with_ns=False)[0]
    if not b in a:
        a.add(b)
        print(b)
    subcats = i.subcategories(recurse=True)
    if next(subcats, False) and next(i.categories().__iter__(), False):
        g = []
        f = set()
        for j in subcats:
            if g:
                g.append(j)
            elif j in f:
                break
            if j == i:
                v.add(i)
                if not g:
                    g = [i]
                else:
                    w.append(g)
                    g = []
                    print(i)
                    break
            f.add(j)
            

f = set()
t = ''
for g in w:
    l = []
    for i in g:
        if i in v:
            l.append(i)
    u = frozenset(l)
    if not u in f:
        f.add(u)
        t += '# ' + ' > '.join(i.title(as_link=True, textlink=True) for i in l) + '\n'

p = pywikibot.Page(s, 'Wikipedie:Údržbové seznamy/Cykly v kategoriích/seznam')
p.text += '\n' + t
p.save(summary='Robot: aktualizace')
