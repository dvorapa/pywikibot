import pywikibot, re

pages = {'Geografie a místopis', 'Hospodářství', 'Humanitní a společenské vědy', 'Kultura a umění', 'Lidé a společnost', 'Ostatní', 'Přírodní vědy', 'Sport', 'Technologie'}
s=pywikibot.Site()

text = ''
for page in pages:
    p=pywikibot.Page(s, 'Wikipedie:Požadované články/' + page)
    text += p.text

links = re.findall(r'\[\[[^\]]*\]\]', text)
seen = {links.pop(0)}
for link in links:
    if not link in seen:
        seen.add(link)
    else:
        print('# ' + link)
