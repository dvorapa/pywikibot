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
from pywikibot import pagegenerators, Page
from pywikibot.bot import (
    ExistingPageBot,
    SingleSiteBot,
)
from pywikibot.textlib import replaceExcept
from urllib.parse import quote_plus


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

    shrnuti = 'aktualizace'

    ################################################################

    mapa = {}
    seznam = []
    duplicity = {}

    ################################################################

    update_options = {
        'summary': 'Robot: ' + shrnuti,  # your own bot summary
        'ref': None,
    }

    def treat_page(self) -> None:
        """Load the given page, do some changes, and save it."""
        objekt_stranky = self.current_page
        text = objekt_stranky.text
        vyjimky = self.vyjimky
        plink = objekt_stranky.title(as_link=True)

        if self.step == 1:
            parametry = re.sub(r'\{\{\{\s*', r'\n{{{', text)
            parametry = re.sub(r'(?m)^((?!\{\{\{).)*$', r'', parametry)
            parametry = re.sub(r'[<|}][^\n]*', r'', parametry)
            parametry = parametry.replace('{{{', '')
            parametry = re.sub(r'(?m)\s*$', r'', parametry)
            parametry = set(filter(None, parametry.split('\n')))
            if '!' in parametry:
                parametry.remove('!')
            self.mapa[plink] = parametry
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
            inTemplate = [0]
            inLink = [False]
            inTable = [False]
            inTag = [False]
            tpage = [None]
            target = [None]
            for part in pageParts:
                match = re.match(r'\{\{\s*((?:[Ii]nfobox[ _]|[Tt]axobox|[Ll]okomotiva[ _]|[Cc]ycling[ _]race\/infobox)[^\|\}]*)', part)
                if match:
                    inTemplate.append(2)
                    tpage.append(Page(self.site, 'Template:' + match.group(1).strip()))
                    if tpage[-1].isRedirectPage():
                        target.append(tpage[-1].getRedirectTarget().title(as_link=True))
                    else:
                        target.append(tpage[-1].title(as_link=True))
                elif part[:2] == '{{':
                    inTemplate.append(1)
                elif part[:1] == '[':
                    inLink.append(True)
                elif part[:2] == '{|':
                    inTable.append(True)
                elif part[:1] == '<':
                    inTag.append(True)

                if inTemplate[-1] == 2 and not inLink[-1] and not inTable[-1] and not inTag[-1]:
                    ################################################################
                    #                            regexy                            #
                    ################################################################

                    # self.opt.parametr
                    # objekt_stranky.title()
                    # with open('soubor.txt', 'a') as soubor:
                    #     soubor.write('# ' + plink + '\n')
                    # part = replaceExcept(part, r'', r'', vyjimky)
                    try:
                        params = re.findall(r'\|\s*([^\=\|\}]+)\s*=\s*([^\|\}]*)', part)
                        known = self.mapa2[target[-1]]
                        tlink = tpage[-1].title(as_link=True)
                        original = tpage[-1].title(with_ns=False)
                        for param, val in params:
                            param = param.strip()
                            if not param in known:
                                self.seznam.append((tlink, original, param, val.strip(), plink))
                                key = original + ':' + param
                                if key not in self.duplicity:
                                    self.duplicity[key] = 1
                                else:
                                    self.duplicity[key] += 1
                    except KeyError:
                        pywikibot.output('# ' + plink + '\t' + target[-1])

                    ################################################################

                if part[-2:] == '}}' and inTemplate[-1] > 0:
                    if inTemplate[-1] == 2:
                        tpage.pop()
                        target.pop()
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
        if arg[1:] == 'ref':
            if re.match(r'[Šš]ablona:', value):
                value = value[8:]
            value = re.escape(value)
            value = value.replace(r'\ ', r'[ _]')
            infobox = r'\{\{\s*[' + value[0].upper() + value[0].lower() + r']' + value[1:] + r' *(?:\||\}\}|<!\-\-|\n)'

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
        gen = pagegenerators.MySQLPageGenerator("select page_namespace, page_title from page where page_namespace like 10 and (page_title like 'Infobox_%' or page_title like 'Taxobox' or page_title like 'Lokomotiva_%' or page_title like 'Cycling_race/infobox') and not page_is_redirect and not page_title like '%/doc'")
        bot = BasicBot(generator=gen, **options)
        bot.infobox = infobox
        bot.step = 1
        bot.run()  # guess what it does
        gen2 = bot.site.allpages(filterredir=False)
        #gen2 = pagegenerators.MySQLPageGenerator("select tl_from_namespace, page_title from templatelinks left join page on tl_from=page_id where tl_from_namespace like 0 and tl_target_id in (select * from (select lt_id from linktarget where lt_namespace like 10 and (lt_title like 'Infobox_%' or lt_title like 'Taxobox' or lt_title like 'Lokomotiva_%' or lt_title like 'Cycling_race/infobox')) as subquery)")
        bot2 = BasicBot(generator=gen2, **options)
        bot2.infobox = infobox
        bot2.step = 2
        bot2.mapa2 = bot.mapa
        bot2.run()  # guess what it does
        page = Page(bot2.site, 'Wikipedie:Údržbové seznamy/Nepodporované parametry infoboxů/seznam')
        page.text = '{| class="wikitable sortable"\n! data-sort-type="number" | Počet výskytů !! Infobox !! Parametr !! Hodnota\n|-\n| '
        seznam = set()
        for template, original, param, val, article in bot2.seznam:
            key = original + ':' + param
            count = bot2.duplicity[key]
            if count > 1:
                seznam.add((str(count) + ' ([https://cs.wikipedia.org/w/index.php?search=hastemplate%3A%22' + quote_plus(original) + '%22+insource%3A%2F%5C%7C+*' + quote_plus(re.escape(param)) + '+*%3D%2F&title=Speci%C3%A1ln%C3%AD%3AHled%C3%A1n%C3%AD&profile=default&fulltext=1])', template, param, ''))
            else:
                seznam.add(('1 (' + article + ')', template, param, '<nowiki>' + val + '</nowiki>'))
        newtext = []
        for article, template, param, val in seznam:
            newtext.append(article + ' || ' + template + ' || ' + param + ' || ' + val)
        newtext.sort()
        page.text += '\n|-\n| '.join(newtext)
        page.text += '\n|}'
        page.save(summary=bot2.opt.summary)


if __name__ == '__main__':
    main()
