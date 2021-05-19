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

import pywikibot, re
from pywikibot import pagegenerators, textlib
from urllib import parse

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

        self.shrnuti = 'aktualizace'

        ################################################################

        self.seznam = ''
        self.seznam2 = ''

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

        # self.opt.parametr
        # self.current_page.title()
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + self.current_page.title(asLink=True) + '\n')
        # part = textlib.replaceExcept(part, r'', r'', self.vyjimky)
        stranka = self.current_page.title(asLink=True)
        kotvy = re.findall(r'\[\[ *([^\#\|\]\n]+)\#([^\|\]\n]+)', text)
        for i, j in kotvy:
            s = pywikibot.Site()
            testovana_stranka = pywikibot.Page(s, i)
            try:
                testovana_stranka.exists()
            except pywikibot.SiteDefinitionError:
                continue
            if testovana_stranka.isRedirectPage():
                testovana_stranka = testovana_stranka.getRedirectTarget()
            if testovana_stranka.exists() or testovana_stranka.is_filepage():
                testovana_stranka.text = textlib.replaceExcept(testovana_stranka.text, r'\[\[[^\|\]\n]+\|([^\]\n]+)\]\]', r'\1', self.vyjimky)
                testovana_stranka.text = textlib.replaceExcept(testovana_stranka.text, r'\[\[([^\|\]\n]+)\]\]', r'\1', self.vyjimky)
                testovana_stranka.text = textlib.replaceExcept(testovana_stranka.text, r' *\{\{ *([Ff]lagicon|[Vv]lajka) *\|[^\}\n]+\}\} *', r'', self.vyjimky)
                testovana_stranka.text = textlib.replaceExcept(testovana_stranka.text, r'( |&nbsp;)', r' ', self.vyjimky)

                nadpis = j.rstrip()
                nadpis = textlib.replaceExcept(nadpis, r'( |&nbsp;)', r' ', self.vyjimky)
                nadpis_wiki = textlib.replaceExcept(nadpis, r'\.([A-Z0-9]{2})', r'%\1', self.vyjimky)
                nadpisy_for = [nadpis, nadpis_wiki]
                nadpisy_if = []
                for n in nadpisy_for:
                    n = parse.unquote(n)
                    n = textlib.replaceExcept(n, r'_', r' ', self.vyjimky)
                    nadpisy_if.append(n)
                nadpisy = []
                for n in nadpisy_if:
                    nadpisy.append(re.compile(r'== *' + re.escape(n) + r' *=='))
                    nadpisy.append(re.compile(r'\{\{ *[Kk]otva *\| *' + re.escape(n) + r' *\}\}'))
                    nadpisy.append(re.compile(r'(name|id)=[\"\']? *' + re.escape(n) + r' *[\"\']?'))
                match = False
                for n in nadpisy:
                    if n.search(testovana_stranka.text):
                        match = True
                        break
                if not match:
                    for n in nadpisy_if:
                        if n.startswith('cite note-'):
                            casti = n.split('-')
                            if casti[-1].isdigit():
                                if int(casti[-1]) <= len(re.findall(r'\<\/ref\>', testovana_stranka.text)):
                                    if len(casti) == 2:
                                        match = True
                                        break
                                    else:
                                        stred = '-'.join(casti[1:-1])
                                        if re.search(r'\<ref *name=[\'\"]? *' + re.escape(stred) + r' *[\'\"]?\>', testovana_stranka.text):
                                            match = True
                                            break
                if not match:
                    self.seznam += '# ' + stranka + '\t[[:' + i.lstrip(':') + '#' + j + ']]\n'
            else:
                self.seznam2 += '# ' + stranka + '\t[[:' + i.lstrip(':') + '#' + j + ']]\n'

        ################################################################

        # if summary option is None, it takes the default i18n summary from
        # i18n subdirectory with summary_key as summary key.
        #self.put_current(text, summary=self.opt.summary if self.opt.summary else 'Robot: ' + self.shrnuti)


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
        page = pywikibot.Page(pywikibot.Site('cs'), 'Wikipedie:Údržbové seznamy/Neexistující kotvy/seznam')
        page.text = bot.seznam.strip()
        page.save(summary=bot.opt.summary if bot.opt.summary else 'Robot: ' + bot.shrnuti)
        page2 = pywikibot.Page(pywikibot.Site('cs'), 'Wikipedie:Údržbové seznamy/Neexistující kotvy/seznam2')
        page2.text = bot.seznam2.strip()
        page2.save(summary=bot.opt.summary if bot.opt.summary else 'Robot: ' + bot.shrnuti)
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False


if __name__ == '__main__':
    main()
