#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
An incomplete sample script.

This is not a complete bot; rather, it is a template from which simple
bots can be made. You can rename it to mybot.py, then edit it in
whatever way you want.

Use global -simulate option for test purposes. No changes to live wiki
will be done.


The following parameters are supported:

-always           The bot won't ask for confirmation when putting a page

-text:            Use this text to be added; otherwise 'Test' is used

-replace:         Don't add text but replace it

-top              Place additional text on top of the page

-summary:         Set the action summary message for the edit.


The following generators and filters are supported:

&params;
"""
#
# (C) Pywikibot team, 2006-2019
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, division, unicode_literals

import pywikibot, re
from pywikibot import pagegenerators, textlib

from pywikibot.bot import (
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)

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
    AutomaticTWSummaryBot,  # Automatically defines summary; needs summary_key
):

    """
    An incomplete sample bot.

    @ivar summary_key: Edit summary message key. The message that should be
        used is placed on /i18n subdirectory. The file containing these
        messages should have the same name as the caller script (i.e. basic.py
        in this case). Use summary_key to set a default edit summary message.

    @type summary_key: str
    """

    summary_key = 'basic-changing'

    def __init__(self, generator, **kwargs):
        """
        Initializer.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        # Add your own options to the bot and set their defaults
        # -always option is predefined by BaseBot class
        self.availableOptions.update({
            'replace': False,  # delete old text and write the new text
            'summary': None,  # your own bot summary
            'text': 'Test',  # add this text from option. 'Test' is default
            'top': False,  # append text on top of the page
        })

        # call initializer of the super class
        super(BasicBot, self).__init__(site=True, **kwargs)

        ################################################################
        #                           výjimky                            #
        ################################################################

        # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
        self.vyjimky = []

        ################################################################
        #                           shrnutí                            #
        ################################################################

        shrnuti = '-substituovaný infobox'

        ################################################################

        self.shrnuti = self.getOption('summary') or 'Robot: ' + shrnuti

        # assign the generator to the bot
        self.generator = generator

    def treat_page(self):
        """Load the given page, do some changes, and save it."""
        text = self.current_page.text

        ################################################################
        #                            změny                             #
        ################################################################

        # self.getOption('parametr')
        # self.current_page.title()
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + self.current_page.title(asLink=True) + '\n')
        text, sep, post = text.partition('|}')
        text = text + sep
        uvod = '''{{substovaný infobox}}
{\| class="infobox"(?:
\|-|)
! colspan="2"(?: bgcolor=#63B8FF|) *\| \'*'''
        podnadpis = '''
\|-
! colspan="2" \| '''
        parametr = r'''(?:\|+\s+|)(?:
\|- *
\| *|)
\|- *
\| \'''([^\']+)\''' *\|\| *'''
        parametr2 = r'''(?:\|+\s+|)(?:
\|- *
\| *|)
\|- *
 *\| *bgcolor *= *"[^\"]+" *\| \'''([^\']+)\''' *\n?\|\|? *'''
        parametr3 = r'''(?:\|+\s+|)(?:
\|- *
\| *|)
\|- *
\| *\|\| *'''
        obrazek = r'''
\|-
! colspan="2" \| *\[\[(?:File|Soubor):([^\|\]]+)\|250px\]\]'''
        zaver = '''(?:
\|-|)
\|}'''
        text = textlib.replaceExcept(text, uvod, r'{{Infobox - MS v hokeji\n | ročník = ', self.vyjimky)
        text = textlib.replaceExcept(text, podnadpis, r'\n| ročník ME = ', self.vyjimky)
        text = textlib.replaceExcept(text, parametr, r'\n| \1 = ', self.vyjimky)
        text = textlib.replaceExcept(text, parametr2, r'\n| \1 = ', self.vyjimky)
        text = textlib.replaceExcept(text, parametr3, r'<br>\n', self.vyjimky)
        text = textlib.replaceExcept(text, obrazek, r'\n| logo = \1', self.vyjimky)
        text = textlib.replaceExcept(text, zaver, r'\n}}', self.vyjimky, count=1)
        text = textlib.replaceExcept(text, r'\| Zlato =', r'| zlato =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Stříbro =', r'| stříbro =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Bronz =', r'| bronz =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Měst[oa] =', r'| města =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Země =[^\|]*\|([^\}]*)[^\n]*', r'| země = \1', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Datum =\s*(.*?\[\[)(\d{4})(\]\])', r'| datum = \1\2\3\n | rok = \2', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Stadion =', r'| arény =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Pořadí =', r'| ročník =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Postup =', r'| postupující =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Sestup =', r'| sestupující =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Počet týmů =', r'| týmy =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Počet zápasů =', r'| zápasy =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Počet gólů =', r'| góly =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Nejužitečnější hráč =', r'| nejhráč =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Nejlepší střelec =', r'| nejstřelec =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Nejlepší nahrávač =', r'| nejnahrávač =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Nejproduktivnější =', r'| nejproduktivnější =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Nejlepší brankář =', r'| nejbrankář =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Kvalifikace =', r'| postupující =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| Návštěvnost =', r'| návštěvnost =', self.vyjimky)
        text = textlib.replaceExcept(text, r'\s*\|\|\s*(\| |\}\})', r'\n \1', self.vyjimky)
        text = textlib.replaceExcept(text, r'\s*\|\|<br>', r'<br>', self.vyjimky)
        text = textlib.replaceExcept(text, r'\s*\'\'\'\s*\| ', r'\n | ', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| ročník( ME|) =\s*(\d+)[^\n]*', r'| ročník\1 = \2', self.vyjimky)
        text = textlib.replaceExcept(text, r'\| sestupující =\s*[Nn]ikdo\s*', r'', self.vyjimky)
        text = text + post

        ################################################################

        # if summary option is None, it takes the default i18n summary from
        # i18n subdirectory with summary_key as summary key.
        self.put_current(text, summary=self.shrnuti)


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: str
    """
    options = {}
    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    gen_factory = pagegenerators.GeneratorFactory()

    # Parse command line arguments
    for arg in local_args:

        # Catch the pagegenerators options
        if gen_factory.handleArg(arg):
            continue  # nothing to do here

        # Now pick up your own options
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
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False


if __name__ == '__main__':
    main()