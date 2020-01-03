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

&params;

-always           The bot won't ask for confirmation when putting a page

-text:            Use this text to be added; otherwise 'Test' is used

-replace:         Dont add text but replace it

-top              Place additional text on top of the page

-summary:         Set the action summary message for the edit.
"""
#
# (C) Pywikibot team, 2006-2018
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

import pywikibot
from pywikibot import pagegenerators, textlib

from pywikibot.bot import (
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
from pywikibot.tools import issue_deprecation_warning

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}


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

        ################################################################
        #                           výjimky                            #
        ################################################################

        # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
        self.vyjimky = []

        ################################################################
        #                           shrnutí                            #
        ################################################################

        self.shrnuti = 'Verze {} uživatele [[Special:Contributions/DvorapaBot|DvorapaBot]] ([[User talk:DvorapaBot|diskuse]]) zrušena'

        ################################################################

        # call initializer of the super class
        super(BasicBot, self).__init__(site=True, **kwargs)

        # handle old -dry parameter
        self._handle_dry_param(**kwargs)

        # assign the generator to the bot
        self.generator = generator

    def _handle_dry_param(self, **kwargs):
        """
        Read the dry parameter and set the simulate variable instead.

        This is a private method. It prints a deprecation warning for old
        -dry paramter and sets the global simulate variable and informs
        the user about this setting.

        The constuctor of the super class ignores it because it is not
        part of self.availableOptions.

        @note: You should ommit this method in your own application.

        @keyword dry: deprecated option to prevent changes on live wiki.
            Use -simulate instead.
        @type dry: bool
        """
        if 'dry' in kwargs:
            issue_deprecation_warning('dry argument',
                                      'pywikibot.config.simulate', 1,
                                      since='20160124')
            # use simulate variable instead
            pywikibot.config.simulate = True
            pywikibot.output('config.simulate was set to True')

    def treat_page(self):
        """Load the given page, do some changes, and save it."""
        text = self.current_page.text

        ################################################################
        #                            regexy                            #
        ################################################################

        # self.getOption('parametr')
        # self.current_page.title()
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + self.current_page.title(asLink=True) + '\n')
        # part = textlib.replaceExcept(part, r'', r'', self.vyjimky)
        seznam = {
            'Triatlon na LOH 2016': 14455477,
            'Kanoistika na LOH 2016': 14455476,
            'Judo na LOH 2012': 14455474,
            'Judo na LOH 2016': 14455473,
            'Fotbal na LOH 2016': 14455472,
            'Box na LOH 2016': 14455471,
            'Atletika na LOH 2016': 14455470,
            'MS v biatlonu 2016': 14455469,
            'MS v biatlonu 2007': 14455468,
            'MS v biatlonu 2011': 14455467,
            'MS v biatlonu 2008': 14455466,
            'MS v biatlonu 2009': 14455465,
            'MS v biatlonu 2012': 14455464,
            'MS v biatlonu 2013': 14455462,
            'MS v biatlonu 2015': 14455461,
            'MS v alpském lyžování 2015': 14455460,
            'Krasobruslení na ZOH 2014': 14455459,
            'Snowboarding na ZOH 2014': 14455458,
            'Curling na ZOH 2014': 14455455,
            'Běh na lyžích na ZOH 2014': 14455453,
            'Akrobatické lyžování na ZOH 2014': 14455452,
            'Biatlon na ZOH 2014': 14455451,
            'Alpské lyžování na ZOH 2014': 14455450,
            'Alpské lyžování na ZOH 2010': 14455449,
            'Běh na lyžích na ZOH 2010': 14455448,
            'Běh na lyžích na ZOH 2006': 14455447,
            'Akrobatické lyžování na ZOH 2002': 14455446,
            'Běh na lyžích na ZOH 2002': 14455445,
            'Běh na lyžích na ZOH 1998': 14455443,
            'Kalendář ZOH 2014': 14455442,
            'Rychlobruslení na ZOH 2014': 14455441,
            'Lední hokej na ZOH 2010': 14455440,
            'Lední hokej na ZOH 1998': 14455439,
            'Lední hokej na ZOH 2006': 14455438,
            'Lední hokej na ZOH 2002': 14455437,
            'MS v atletice 2013': 14455436,
            'Atletika na LOH 1904': 14455435,
            'Atletika na LOH 1896': 14455434,
            'Atletika na LOH 1900': 14455433,
            'Atletika na LOH 1908': 14455430,
            'Zápas na LOH 1976': 14455429,
            'Atletika na LOH 1912': 14455428,
            'Atletika na LOH 1920': 14455427,
            'Atletika na LOH 1924': 14455425,
            'Atletika na LOH 1928': 14455424,
            'Atletika na LOH 1932': 14455423,
            'Atletika na LOH 1936': 14455422,
            'Atletika na LOH 1948': 14455421,
            'Atletika na LOH 1952': 14455420,
            'Atletika na LOH 1956': 14455419,
            'Atletika na LOH 1960': 14455418,
            'Atletika na LOH 1964': 14455416,
            'Zápas na LOH 1936': 14455414,
            'MS v alpském lyžování 2013': 14455412,
            'Atletika na LOH 2000': 14455411,
            'Atletika na LOH 1968': 14455410,
            'Atletika na LOH 1996': 14455409,
            'Atletika na LOH 1992': 14455408,
            'Atletika na LOH 1988': 14455406,
            'Atletika na LOH 1984': 14455405,
            'Atletika na LOH 1980': 14455404,
            'Atletika na LOH 1976': 14455403,
            'Kanoistika na LOH 1972': 14455402,
            'Atletika na LOH 1972': 14455401,
            'Atletika na LOH 2004': 14455400,
            'Kanoistika na LOH 1992': 14455399,
            'Kanoistika na LOH 1996': 14455398,
            'Kanoistika na LOH 2000': 14455397,
            'Kanoistika na LOH 2004': 14455396,
            'Kanoistika na LOH 2008': 14455395,
            'Kanoistika na LOH 2012': 14455388,
            'Lední hokej na ZOH 2014': 14455387,
            'Atletika na LOH 2012': 14455386,
            'Rychlobruslení na ZOH 2002': 14455385,
            'Rychlobruslení na ZOH 2006': 14455384,
            'Vzpírání na LOH 2012': 14455383,
            'Zápas na LOH 1968': 14455382,
            'Fotbal na LOH 2012': 14455381,
            'Fotbal na LOH 2004': 14455380,
            'Fotbal na LOH 2000': 14455379,
            'Fotbal na LOH 1996': 14455378,
            'MS v atletice 2011': 14455377,
            'Zápas na LOH 1980': 14455375,
            'MS v alpském lyžování 2011': 14455374,
            'Zápas na LOH 1972': 14455373,
            'Zápas na LOH 1992': 14455372,
            'Zápas na LOH 1988': 14455371,
            'Zápas na LOH 1984': 14455368,
            'Rychlobruslení na ZOH 2010': 14455366,
            'Plavání na LOH 2008': 14455364,
            'Taekwondo na LOH 2008': 14455363,
            'Atletika na LOH 2008': 14455362,
            'Fotbal na LOH 2008': 14455361,
            'Triatlon na LOH 2008': 14455360,
            'Sportovní střelba na LOH 2008': 14455359,
            'Vzpírání na LOH 2008': 14455358            
        }

        revize = seznam[self.current_page.title(withNamespace=False)]
        historie = list(self.current_page.revisions())
        prev = 0
        for r in historie:
            if prev == 1:
                break
            if r['revid'] == revize:
                prev = 1

        stary_text = self.current_page.getOldVersion(r['revid'])
        kategorie = textlib.getCategoryLinks(stary_text)
        text += '<noinclude>\n' + '\n'.join(i.aslink() for i in kategorie) + '\n</noinclude>'
        text = textlib.replaceExcept(text, r'Kategorie *: *Šablony [-–] ', r'Kategorie:Šablony:', self.vyjimky)
        text = textlib.replaceExcept(text, r'\|\{\{PAGENAME\}\}\]\]', r']]', self.vyjimky)
        text = textlib.replaceExcept(text, r'\s*<\/noinclude>\s*<noinclude>\s*', r'\n', self.vyjimky)

        ################################################################

        # if summary option is None, it takes the default i18n summary from
        # i18n subdirectory with summary_key as summary key.
        self.put_current(text, summary=self.getOption('summary') if self.getOption('summary') else 'Robot: ' + self.shrnuti.format(revize))


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
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
