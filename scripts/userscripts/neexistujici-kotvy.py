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
from pywikibot.exceptions import SiteDefinitionError, InvalidTitleError
from urllib.parse import unquote


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
    vyjimky = tuple()

    ################################################################
    #                           shrnutí                            #
    ################################################################

    shrnuti = 'aktualizace'

    ################################################################

    seznam = []
    seznam2 = []

    ################################################################

    update_options = {
        'summary': 'Robot: ' + shrnuti,  # your own bot summary
    }

    def treat_page(self) -> None:
        """Load the given page, do some changes, and save it."""
        objekt_stranky = self.current_page
        text = objekt_stranky.text

        ################################################################
        #                            změny                             #
        ################################################################

        # If you find out that you do not want to edit this page, just return.
        # self.opt.parametr (nebo self.opt['parametr'])
        # objekt_stranky.title()
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + stranka + '\n')
        # part = replaceExcept(part, r'', r'', vyjimky)
        stranka = objekt_stranky.title(as_link=True)
        kotvy = re.findall(r'\[\[ *([^\#\|\]\n]+)\#([^\|\]\n]+)', text)
        vyjimky = self.vyjimky
        re_compile = re.compile
        re_escape = re.escape
        for cil, kotva in kotvy:
            test_stranka = Page(self.site, cil)
            try:
                test_str_existuje = test_stranka.exists()
            except (SiteDefinitionError, InvalidTitleError):
                continue
            if test_stranka.isRedirectPage():
                test_stranka = pywikibot.Page(self.site, test_stranka.getRedirectTarget().title(with_section=False))
            if test_str_existuje or test_stranka.is_filepage():
                text_stranky = test_stranka.text
                text_stranky = replaceExcept(text_stranky, r'\[\[[^\|\]\n]+\|([^\]\n]+)\]\]', r'\1', vyjimky)
                text_stranky = replaceExcept(text_stranky, r'\[\[([^\|\]\n]+)\]\]', r'\1', vyjimky)
                text_stranky = replaceExcept(text_stranky, r' *\{\{ *(?:[Ff]lagicon|[Vv]lajka) *\|[^\}\n]+\}\} *', r'', vyjimky)
                text_stranky = replaceExcept(text_stranky, r'(?: |&nbsp;)', r' ', vyjimky)

                nadpis = kotva.rstrip()
                nadpis = replaceExcept(nadpis, r'(?: |&nbsp;)', r' ', vyjimky)
                nadpis_wiki = replaceExcept(nadpis, r'\.([A-Z0-9]{2})', r'%\1', vyjimky)
                nadpisy_for = (nadpis, nadpis_wiki)
                nadpisy_if = []
                for n in nadpisy_for:
                    n = unquote(n)
                    n = replaceExcept(n, r'_', r' ', vyjimky)
                    nadpisy_if.append(n)
                nadpisy = []
                nadpisy_append = nadpisy.append
                for n in nadpisy_if:
                    nadpisy_append(re_compile(r'== *' + re_escape(n) + r' *=='))
                    nadpisy_append(re_compile(r'\{\{ *[Kk]otva *\| *' + re_escape(n) + r' *\}\}'))
                    nadpisy_append(re_compile(r'(?:name|id)=[\"\']? *' + re_escape(n) + r' *[\"\']?'))
                match = False
                for n in nadpisy:
                    if n.search(text_stranky):
                        match = True
                        break
                if not match:
                    for n in nadpisy_if:
                        if n.startswith('cite note-'):
                            casti = n.split('-')
                            if casti[-1].isdigit():
                                if int(casti[-1]) <= len(re.findall(r'\<\/ref\>', text_stranky)):
                                    if len(casti) == 2 or re.search(r'\<ref *name=[\'\"]? *' + re_escape('-'.join(casti[1:-1])) + r' *[\'\"]?\>', text_stranky):
                                        match = True
                                        break
                if not match:
                    self.seznam.append(stranka + '\t[[:' + cil.lstrip(':') + '#' + kotva)
            else:
                self.seznam2.append(stranka + '\t[[:' + cil.lstrip(':') + '#' + kotva)

        ################################################################

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
        bot.run()  # guess what it does
        page = Page(bot.site, 'Wikipedie:Údržbové seznamy/Neexistující kotvy/seznam')
        page.text = '# ' + ']]\n# '.join(bot.seznam) + ']]'
        page.save(summary=bot.opt.summary)
        page2 = Page(bot.site, 'Wikipedie:Údržbové seznamy/Neexistující kotvy/seznam2')
        page2.text = '# ' + ']]\n# '.join(bot.seznam2) + ']]'
        page2.save(summary=bot.opt.summary)


if __name__ == '__main__':
    main()
