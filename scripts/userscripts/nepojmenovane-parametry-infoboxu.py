#!/usr/bin/env python3
"""
An incomplete sample script.

This is not a complete bot; rather, it is a template from which simple
bots can be made. You can rename it to mybot.py, then edit it in
whatever way you want.

Use global -simulate option for test purposes. No changes to live wiki
will be done.


The following parameters are supported:

-always           The bot won't ask for confirmation when putting a page

-summary:         Set the action summary message for the edit.

In addition the following generators and filters are supported but
cannot be set by settings file:

&params;
"""
#
# (C) Pywikibot team, 2006-2022
#
# Distributed under the terms of the MIT license.
#
from __future__ import annotations

import pywikibot, re
from pywikibot import pagegenerators
from pywikibot.bot import (
    ExistingPageBot,
    SingleSiteBot,
)
from pywikibot.textlib import replaceExcept


# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {'&params;': pagegenerators.parameterHelp}  # noqa: N816


class BasicBot(
    # Refer pywikobot.bot for generic bot classes
    SingleSiteBot,  # A bot only working on one site
    # CurrentPageBot,  # Sets 'current_page'. Process it in treat_page method.
    #                  # Not needed here because we have subclasses
    ExistingPageBot,  # CurrentPageBot which only treats existing pages
):

    """
    An incomplete sample bot.
    """

    use_redirects = False  # treats non-redirects only

    ################################################################
    #                           výjimky                            #
    ################################################################

    # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
    vyjimky = ['nowiki']

    ################################################################
    #                           shrnutí                            #
    ################################################################

    shrnuti = '-prázdné nepojmenované parametry infoboxu'

    ################################################################

    gen2 = set()
    gen3 = []
    seznam = []

    ################################################################

    update_options = {
        'summary': 'Robot: ' + shrnuti,  # your own bot summary
        'ref': None,
    }

    infobox = opt.ref
    if re.match(r'[Šš]ablona:', infobox):
        infobox = infobox[8:]
    infobox = re.escape(infobox)
    infobox = infobox.replace(r'\ ', r'[ _]')
    infobox = r'\{\{\s*[' + infobox[0].upper() + infobox[0].lower() + r']' + infobox[1:] + r' *(?:\||\}\}|<!\-\-|\n)'

    def treat_page(self) -> None:
        """Load the given page, do some changes, and save it."""
        objekt_stranky = self.current_page
        text = objekt_stranky.text
        vyjimky = self.vyjimky

        if self.step == 1:
            text = replaceExcept(text, r'\{\{', r'ßßß{{', vyjimky)
            text = replaceExcept(text, r'\}\}', r'}}ßßß', vyjimky)
            text = replaceExcept(text, r'(\[+)', r'ßßß\1', vyjimky)
            text = replaceExcept(text, r'(\]{1,2})', r'\1ßßß', vyjimky)
            text = replaceExcept(text, r'\{\|', r'ßßß{|', vyjimky)
            text = replaceExcept(text, r'\|\}([^\}])', r'|}ßßß\1', vyjimky)
            text = replaceExcept(text, r'\<', r'ßßß<', vyjimky)
            text = replaceExcept(text, r'\>', r'>ßßß', vyjimky)
            pageParts = text.strip('ß').split('ßßß')
            inTemplate = [0]
            inLink = [False]
            inTable = [False]
            inTag = [False]
            noRemoveEmptyUnnamed = False
            for part in pageParts:
                if re.match(r'\{\{ *(?:Infobox |NFPA 704|Studenti píší Wikipedii|Taxobox|Singly|Expedice-start a přistání|F1 Grand Prix|Kosmické těleso-(?:dceřiné těleso|teleskop)|Turnaj Grand Slamu)', part, flags=re.I) and not re.match(r'\{\{ *(?:Infobox (?:začátek|hlavička|obrázek|dvojitá|jednoduchá|konec|položka|chybí|Ročník fotbalového turnaje\/Fb|Eurovision\/Legenda|animanga\/Patička|- (?:železniční trať\/(?:legenda|hlavička)|číslo\/řada|politická strana\/mandáty|letiště\/(?:RWY|Konec)|budova\/kodbarvy|chemický prvek\/(?:Legenda|Barva|Text|Skupina|Izotopy)))|Taxobox\/(?:barva|cat|compare|Stupeň ohrožení|statusWD))', part, flags=re.I):
                    inTemplate.append(2)
                    if re.match(r'\{\{ *(?:Turnaj Grand Slamu|Infobox - t(?:urnaj Grand Slamu|enis(?: na LOH|ová soutěž)))', part, flags=re.I):
                        noRemoveEmptyUnnamed = True
                elif part[:2] == '{{':
                    inTemplate.append(1)
                elif part[:1] == '[':
                    inLink.append(True)
                elif part[:2] == '{|':
                    inTable.append(True)
                elif part[:1] == '<':
                    inTag.append(True)

                if inTemplate[-1] == 2 and not inLink[-1] and not inTable[-1] and not inTag[-1] and not noRemoveEmptyUnnamed:
                    if re.search(r'\|\s*[\|\}]', part):
                        self.gen2.add(objekt_stranky)
                        self.gen3.append(objekt_stranky)
                    elif re.search(r'\|(?:\s*=|\s*[0-9]+\s*=)?[^\|\}\=]*(?:\||\}|$)', part):
                        self.gen3.append(objekt_stranky)

                if part[-2:] == '}}' and inTemplate[-1] > 0:
                    if inTemplate[-1] == 2:
                        noRemoveEmptyUnnamed = False
                    inTemplate.pop()
                elif part[-1:] == ']' and inLink[-1]:
                    inLink.pop()
                elif part[-2:] == '|}' and inTable[-1]:
                    inTable.pop()
                elif part[-1:] == '>' and inTag[-1]:
                    inTag.pop()
        elif self.step == 2:
            text = replaceExcept(text, r'\{\{', r'ßßß{{', vyjimky)
            text = replaceExcept(text, r'\}\}', r'}}ßßß', vyjimky)
            text = replaceExcept(text, r'(\[+)', r'ßßß\1', vyjimky)
            text = replaceExcept(text, r'(\]{1,2})', r'\1ßßß', vyjimky)
            text = replaceExcept(text, r'\{\|', r'ßßß{|', vyjimky)
            text = replaceExcept(text, r'\|\}([^\}])', r'|}ßßß\1', vyjimky)
            text = replaceExcept(text, r'\<', r'ßßß<', vyjimky)
            text = replaceExcept(text, r'\>', r'>ßßß', vyjimky)
            pageParts = text.strip('ß').split('ßßß')
            newPageParts = []
            inTemplate = [0]
            inLink = [False]
            inTable = [False]
            inTag = [False]
            afterBlockTemplate = False
            noNewLineAfterBlockTemplate = False
            initialSpaces = 1
            for part in pageParts:
                if re.match(r'\{\{ *(?:Infobox |NFPA 704|Studenti píší Wikipedii|Taxobox|Singly|Expedice-start a přistání|F1 Grand Prix|Kosmické těleso-(?:dceřiné těleso|teleskop)|Turnaj Grand Slamu)', part, flags=re.I) and not re.match(r'\{\{ *(?:Infobox (?:začátek|hlavička|obrázek|dvojitá|jednoduchá|konec|položka|chybí|Ročník fotbalového turnaje\/Fb|Eurovision\/Legenda|animanga\/Patička|- (?:železniční trať\/(?:legenda|hlavička)|číslo\/řada|politická strana\/mandáty|letiště\/(?:RWY|Konec)|budova\/kodbarvy|chemický prvek\/(?:Legenda|Barva|Text|Skupina|Izotopy)))|Taxobox\/(?:barva|cat|compare|Stupeň ohrožení|statusWD))', part, flags=re.I):
                    inTemplate.append(2)
                    if re.match(r'\{\{ *Infobox - chemický prvek\/(?:Nestabilní izotop|Stabilní izotop)', part, flags=re.I):
                        noNewLineAfterBlockTemplate = True
                    if re.match(r'[^\n]+\n+ *\|', part):
                        initialSpaces = len(re.match(r'[^\n]+\n+( *)\|', part).group(1))
                elif part[:2] == '{{':
                    inTemplate.append(1)
                elif part[:1] == '[':
                    inLink.append(True)
                elif part[:2] == '{|':
                    inTable.append(True)
                elif part[:1] == '<':
                    inTag.append(True)

                if afterBlockTemplate:
                    part = replaceExcept(part, r'^\s*', r'\n', vyjimky)
                    afterBlockTemplate = False
                if inTemplate[-1] == 2 and not inLink[-1] and not inTable[-1] and not inTag[-1]:
                    part = replaceExcept(part, r'\|\s*(?=\||\})', r'', vyjimky)
                    part = replaceExcept(part, r'\s*\|\s*', r'\n' + r' '*initialSpaces + r'| ', vyjimky)
                    part = replaceExcept(part, r'\{\{\s*', r'{{', vyjimky)
                    if part[:2] == '{{' and not '|' in part:
                        part = replaceExcept(part, r'\s*\}\}', r'}}', vyjimky)
                    else:
                        part = replaceExcept(part, r'\s*\}\}', r'\n}}', vyjimky)
                    part = replaceExcept(part, r'\|([^=\|\}]*?)\s*=[ \t]*', r'|\1 = ', vyjimky)
                    if not re.search(r'\#[0-9a-fA-F]{3,6}', part) or not re.search(r'odkaz na (?:konečné pořadí|statistiky turnaje)', part):
                        part = replaceExcept(part, r'=\s*(\*|\#)', r'=\n\1', vyjimky)
                newPageParts.append(part)

                if part[-2:] == '}}' and inTemplate[-1] > 0:
                    if inTemplate[-1] == 2:
                        if not noNewLineAfterBlockTemplate:
                            afterBlockTemplate = True
                        else:
                            noNewLineAfterBlockTemplate = False
                        initialSpaces = 1
                    inTemplate.pop()
                elif part[-1:] == ']' and inLink[-1]:
                    inLink.pop()
                elif part[-2:] == '|}' and inTable[-1]:
                    inTable.pop()
                elif part[-1:] == '>' and inTag[-1]:
                    inTag.pop()
            text = ''.join(newPageParts)
            self.put_current(text, summary=self.opt.summary)
        elif self.step == 3:
            text = replaceExcept(text, r'\{\{', r'ßßß{{', vyjimky)
            text = replaceExcept(text, r'\}\}', r'}}ßßß', vyjimky)
            text = replaceExcept(text, r'(\[+)', r'ßßß\1', vyjimky)
            text = replaceExcept(text, r'(\]{1,2})', r'\1ßßß', vyjimky)
            text = replaceExcept(text, r'\{\|', r'ßßß{|', vyjimky)
            text = replaceExcept(text, r'\|\}([^\}])', r'|}ßßß\1', vyjimky)
            text = replaceExcept(text, r'\<', r'ßßß<', vyjimky)
            text = replaceExcept(text, r'\>', r'>ßßß', vyjimky)
            pageParts = text.strip('ß').split('ßßß')
            inTemplate = [0]
            blockTemplate=['']
            inLink = [False]
            inTable = [False]
            inTag = [False]
            noRemoveEmptyUnnamed = False
            for part in pageParts:
                if re.match(r'\{\{ *(?:Infobox |NFPA 704|Studenti píší Wikipedii|Taxobox|Singly|Expedice-start a přistání|F1 Grand Prix|Kosmické těleso-(?:dceřiné těleso|teleskop)|Turnaj Grand Slamu)', part, flags=re.I) and not re.match(r'\{\{ *(?:Infobox (?:začátek|hlavička|obrázek|dvojitá|jednoduchá|konec|položka|chybí|Ročník fotbalového turnaje\/Fb|Eurovision\/Legenda|animanga\/Patička|- (?:železniční trať\/(?:legenda|hlavička)|číslo\/řada|politická strana\/mandáty|letiště\/(?:RWY|Konec)|budova\/kodbarvy|chemický prvek\/(?:Legenda|Barva|Text|Skupina|Izotopy)))|Taxobox\/(?:barva|cat|compare|Stupeň ohrožení|statusWD))', part, flags=re.I):
                    inTemplate.append(2)
                    blockTemplate.append(part.strip('{}').split('|')[0].strip())
                    if re.match(r'\{\{ *(?:Turnaj Grand Slamu|Infobox - t(?:urnaj Grand Slamu|enis(?: na LOH|ová soutěž)))', part, flags=re.I):
                        noRemoveEmptyUnnamed = True
                elif part[:2] == '{{':
                    inTemplate.append(1)
                elif part[:1] == '[':
                    inLink.append(True)
                elif part[:2] == '{|':
                    inTable.append(True)
                elif part[:1] == '<':
                    inTag.append(True)

                if inTemplate[-1] == 2 and not inLink[-1] and not inTable[-1] and not inTag[-1] and not noRemoveEmptyUnnamed:
                    if re.search(r'\|(?:\s*=|\s*[0-9]+\s*=)?[^\|\}\=]*(?:\||\}|$)', part):
                        nalezene = re.findall(r'\|((?:\s*=|\s*[0-9]+\s*=)?[^\|\}\=]*)$', part)
                        nalezene = [s + '/šablona, odkaz, tabulka nebo tag/' for s in nalezene]
                        nalezene += re.findall(r'(?=\|((?:\s*=|\s*[0-9]+\s*=)?[^\|\}\=]*)[\|\}])', part)
                        nalezene = [s.strip().replace('\n', '↵') for s in nalezene]
                        self.seznam.append(objekt_stranky.title(as_link=True) + '\t' + blockTemplate[-1] + '\t' + '; '.join(nalezene))

                if part[-2:] == '}}' and inTemplate[-1] > 0:
                    if inTemplate[-1] == 2:
                        blockTemplate.pop()
                        noRemoveEmptyUnnamed = False
                    inTemplate.pop()
                elif part[-1:] == ']' and inLink[-1]:
                    inLink.pop()
                elif part[-2:] == '|}' and inTable[-1]:
                    inTable.pop()
                elif part[-1:] == '>' and inTag[-1]:
                    inTag.pop()

        # if summary option is None, it takes the default i18n summary from
        # i18n subdirectory with summary_key as summary key.
        #self.put_current(text, summary=self.opt.summary)


def main(*args: str) -> None:
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    :param args: command line arguments
    """
    options = {}
    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    gen_factory = pagegenerators.GeneratorFactory()

    for arg in local_args:
        arg, _, value = arg.partition(':')
        option = arg[1:]
        if option == 'ref':
            options[option] = value

    # Process pagegenerators arguments
    local_args = gen_factory.handle_args(local_args)

    # Parse your own command line arguments
    for arg in local_args:
        arg, _, value = arg.partition(':')
        option = arg[1:]
        if option in ('summary', 'text'):
            if not value:
                pywikibot.input('Please enter a value for ' + arg)
            options[option] = value
        # take the remaining options as booleans.
        # You will get a hint if they aren't pre-defined in your bot class
        else:
            options[option] = True

    # The preloading option is responsible for downloading multiple
    # pages from the wiki simultaneously.
    gen = gen_factory.getCombinedGenerator(preload=True)

    # check if further help is needed
    if not pywikibot.bot.suggest_help(missing_generator=not gen):
        # pass generator and private options to the bot
        bot = BasicBot(generator=gen, **options)
        bot.step = 1
        bot.run()
        bot2 = BasicBot(generator=bot.gen2, **options)
        bot2.step = 2
        bot2.run()
        bot3 = BasicBot(generator=bot.gen3, **options)
        bot3.step = 3
        bot3.run()
        page = pywikibot.Page(bot.site, 'Wikipedie:Údržbové seznamy/Nepojmenované parametry infoboxů/seznam')
        page.text = '# ' + '\n# '.join(bot3.seznam)
        page.save(summary='Robot: aktualizace')


if __name__ == '__main__':
    main()
