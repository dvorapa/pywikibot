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

from collections import OrderedDict

from poradi import poradi

import pywikibot
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

        ################################################################
        #                           výjimky                            #
        ################################################################

        # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
        self.vyjimky = []

        ################################################################
        #                           shrnutí                            #
        ################################################################

        self.shrnuti = 'správné pořadí sekcí'

        ################################################################

        # call initializer of the super class
        super(BasicBot, self).__init__(site=True, **kwargs)

        # assign the generator to the bot
        self.generator = generator

    def treat_page(self):
        """Load the given page, do some changes, and save it."""
        text = self.current_page.text

        ################################################################
        #                            skript                            #
        ################################################################

        # self.getOption('parametr')
        # self.current_page.title()
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + self.current_page.title(as_link=True) + '\n')
        # text = textlib.replaceExcept(text, r'', r'', self.vyjimky)
        h = '*'
        assert isinstance(poradi, list)
        assert h in poradi
        poradi_list = [kopie for kopie in poradi]
        poradi_list.remove(h)
        assert h not in poradi_list
        del poradi_list

        index = poradi.index(h)
        pred = poradi[:index]
        pred.reverse()
        za = poradi[index+1:]

        uvod, stat, zaver = textlib.extract_sections(text, self.current_page.site)
        stat_dict = dict(stat)

        for sekce in pred:
            if sekce in stat_dict:
                presunovana = (sekce, stat_dict[sekce])
                stat.remove(presunovana)
                stat.insert(0, presunovana)

        for sekce in za:
            if sekce in stat_dict:
                presunovana = (sekce, stat_dict[sekce])
                stat.remove(presunovana)
                stat.insert(-1, presunovana)

        text = uvod + ''.join([i + j for i, j in stat]) + zaver

        ################################################################

        # if summary option is None, it takes the default i18n summary from
        # i18n subdirectory with summary_key as summary key.
        self.put_current(text, summary=self.getOption('summary') if self.getOption('summary') else 'Robot: ' + self.shrnuti)


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
        if gen_factory.handle_arg(arg):
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
