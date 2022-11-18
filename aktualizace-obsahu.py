#!/usr/bin/env python3
import pywikibot

from pywikibot import textlib

s = pywikibot.Site()

o = pywikibot.Page(s, 'Diskuse s wikipedistou:Dvorapa/Obsah')
ot = o.text
odkazu = ot.count('<li')

nadpisy = textlib._extract_headings(pywikibot.Page(s, 'Diskuse s wikipedistou:Dvorapa').text, s)
rozdil = len(nadpisy) - odkazu
if rozdil:
  pred, ul, po = ot.partition('</ul>')
  for c, n in enumerate(nadpisy[-rozdil:], 1):
    pred += '<li class="toclevel-1"><span class="tocnumber">{cislo}</span> <span class="toctext">[[#{titulek}|{titulek}]]</span></li>\n'.format(cislo=odkazu + c, titulek=n[0].strip(' ='))
  o.text = pred + ul + po
  o.save(summary='Robot: přidána sekce' if rozdil == 1 else 'Robot: přidány sekce')
