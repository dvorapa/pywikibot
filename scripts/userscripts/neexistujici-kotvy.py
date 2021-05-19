#!/usr/bin/python
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

All settings can be made by giving option with the command line.

In addition the following generators and filters are supported:

&params;
"""
#
# (C) Pywikibot team, 2006-2021
#
# Distributed under the terms of the MIT license.
#
import pywikibot, re
from pywikibot import pagegenerators, Page
from pywikibot.backports import Tuple
from pywikibot.bot import (
    ExistingPageBot,
    NoRedirectPageBot,
    SingleSiteBot,
)
from pywikibot.textlib import replaceExcept
from pywikibot.exceptions import SiteDefinitionError
from urllib import parse


# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {'&params;': pagegenerators.parameterHelp}  # noqa: N816


class BasicBot(
    # Refer pywikobot.bot for generic bot classes
    SingleSiteBot,  # A bot only working on one site
    # CurrentPageBot,  # Sets 'current_page'. Process it in treat_page method.
    #                  # Not needed here because we have subclasses
    ExistingPageBot,  # CurrentPageBot which only treats existing pages
    NoRedirectPageBot,  # CurrentPageBot which only treats non-redirects
):

    """
    An incomplete sample bot.
    """

    def __init__(self, generator, **kwargs) -> None:
        """
        Initializer.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        # Add your own options to the bot and set their defaults
        # -always option is predefined by BaseBot class
        self.available_options.update({
            'summary': None,  # your own bot summary
        })

        ################################################################
        #                           výjimky                            #
        ################################################################

        # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
        self.vyjimky = tuple()

        ################################################################
        #                           seznamy                            #
        ################################################################

        self.seznam = []
        self.seznam2 = []

        ################################################################

        # call initializer of the super class
        super().__init__(site=True, **kwargs)
        # assign the generator to the bot
        self.generator = generator

    def treat_page(self) -> None:
        """Load the given page, do some changes, and save it."""
        objekt_stranky = self.current_page
        text = objekt_stranky.text

        ################################################################
        #                            regexy                            #
        ################################################################

        # self.opt.parametr nebo self.opt['parametr']
        # objekt_stranky.title()
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + objekt_stranky.title(as_link=True) + '\n')
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
            except SiteDefinitionError:
                continue
            if test_stranka.isRedirectPage():
                test_stranka = test_stranka.getRedirectTarget()
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
                    n = parse.unquote(n)
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


def main(*args: Tuple[str, ...]) -> None:
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
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
        arg, sep, value = arg.partition(':')
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
    if gen:
        # pass generator and private options to the bot
        bot = BasicBot(gen, **options)
        bot.run()  # guess what it does
        page = Page(bot.site, 'Wikipedie:Údržbové seznamy/Neexistující kotvy/seznam')
        page.text = '# ' + ']]\n# '.join(bot.seznam) + ']]'
        shrnuti = 'Robot: aktualizace'
        page.save(summary=bot.opt.summary or shrnuti)
        page2 = Page(bot.site, 'Wikipedie:Údržbové seznamy/Neexistující kotvy/seznam2')
        page2.text = '# ' + ']]\n# '.join(bot.seznam2) + ']]'
        page2.save(summary=bot.opt.summary or shrnuti)
    else:
        pywikibot.bot.suggest_help(missing_generator=True)


if __name__ == '__main__':
    main()
