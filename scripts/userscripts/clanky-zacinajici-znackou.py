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

import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import (
    ExistingPageBot,
    SingleSiteBot,
)
from re import match


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

    ################################################################

    update_options = {
        'summary': 'Robot: ' + shrnuti,  # your own bot summary
    }

    def treat_page(self) -> None:
        """Load the given page, do some changes, and save it."""
        stranka = self.current_page
        text = stranka.text

        ################################################################
        #                            změny                             #
        ################################################################

        # If you find out that you do not want to edit this page, just return.
        # self.opt.parametr (nebo self.opt['parametr'])
        # stranka.title()
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + stranka.title(as_link=True) + '\n')
        # text = textlib.replaceExcept(text, r'', r'', self.vyjimky)
        predloha = r'(?:\s*(?:{{[^{}]*}}|\[\[\s*(?:' + r'|'.join(self.site.namespaces.FILE) + r')[^\[\]]*\]\]|<!--(?:[^-]|-[^-]|--[^>])-->))*\s*<[^!]'
        if match(predloha, text):
            self.seznam.append(stranka.title(as_link=True))

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
        page = pywikibot.Page(bot.site, 'Wikipedie:Údržbové seznamy/Články začínající značkou/seznam')
        page.text = '# ' + '\n# '.join(bot.seznam)
        page.save(summary=bot.opt.summary)


if __name__ == '__main__':
    main()
