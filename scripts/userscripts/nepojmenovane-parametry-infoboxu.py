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

    def __init__(self, generator, step, **kwargs):
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
        self.vyjimky = ['nowiki']

        ################################################################
        #                           shrnutí                            #
        ################################################################

        self.shrnuti = '-prázdné nepojmenované parametry infoboxu'

        ################################################################

        self.step = step
        if self.step == 1:
            self.gen2 = set()
            self.gen3 = []
        elif self.step == 3:
            self.seznam = ''

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

        if self.step == 1:
            text = textlib.replaceExcept(text, r'\{\{', r'ßßß{{', self.vyjimky)
            text = textlib.replaceExcept(text, r'\}\}', r'}}ßßß', self.vyjimky)
            text = textlib.replaceExcept(text, r'(\[+)', r'ßßß\1', self.vyjimky)
            text = textlib.replaceExcept(text, r'(\]{1,2})', r'\1ßßß', self.vyjimky)
            text = textlib.replaceExcept(text, r'\{\|', r'ßßß{|', self.vyjimky)
            text = textlib.replaceExcept(text, r'\|\}([^\}])', r'|}ßßß\1', self.vyjimky)
            text = textlib.replaceExcept(text, r'\<', r'ßßß<', self.vyjimky)
            text = textlib.replaceExcept(text, r'\>', r'>ßßß', self.vyjimky)
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
                        self.gen2.add(self.current_page)
                        self.gen3.append(self.current_page)
                    elif re.search(r'\|(?:\s*=|\s*[0-9]+\s*=)?[^\|\}\=]*(?:\||\}|$)', part):
                        self.gen3.append(self.current_page)

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
            text = textlib.replaceExcept(text, r'\{\{', r'ßßß{{', self.vyjimky)
            text = textlib.replaceExcept(text, r'\}\}', r'}}ßßß', self.vyjimky)
            text = textlib.replaceExcept(text, r'(\[+)', r'ßßß\1', self.vyjimky)
            text = textlib.replaceExcept(text, r'(\]{1,2})', r'\1ßßß', self.vyjimky)
            text = textlib.replaceExcept(text, r'\{\|', r'ßßß{|', self.vyjimky)
            text = textlib.replaceExcept(text, r'\|\}([^\}])', r'|}ßßß\1', self.vyjimky)
            text = textlib.replaceExcept(text, r'\<', r'ßßß<', self.vyjimky)
            text = textlib.replaceExcept(text, r'\>', r'>ßßß', self.vyjimky)
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
                    part = textlib.replaceExcept(part, r'^\s*', r'\n', self.vyjimky)
                    afterBlockTemplate = False
                if inTemplate[-1] == 2 and not inLink[-1] and not inTable[-1] and not inTag[-1]:
                    part = textlib.replaceExcept(part, r'\|\s*(?=\||\})', r'', self.vyjimky)
                    part = textlib.replaceExcept(part, r'\s*\|\s*', r'\n' + r' '*initialSpaces + r'| ', self.vyjimky)
                    part = textlib.replaceExcept(part, r'\{\{\s*', r'{{', self.vyjimky)
                    if part[:2] == '{{' and not '|' in part:
                        part = textlib.replaceExcept(part, r'\s*\}\}', r'}}', self.vyjimky)
                    else:
                        part = textlib.replaceExcept(part, r'\s*\}\}', r'\n}}', self.vyjimky)
                    part = textlib.replaceExcept(part, r'\|([^=\|\}]*?)\s*=[ \t]*', r'|\1 = ', self.vyjimky)
                    if not re.search(r'\#[0-9a-fA-F]{3,6}', part) or not re.search(r'odkaz na (?:konečné pořadí|statistiky turnaje)', part):
                        part = textlib.replaceExcept(part, r'=\s*(\*|\#)', r'=\n\1', self.vyjimky)
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
            self.put_current(text, summary=self.getOption('summary') if self.getOption('summary') else 'Robot: ' + self.shrnuti)
        elif self.step == 3:
            text = textlib.replaceExcept(text, r'\{\{', r'ßßß{{', self.vyjimky)
            text = textlib.replaceExcept(text, r'\}\}', r'}}ßßß', self.vyjimky)
            text = textlib.replaceExcept(text, r'(\[+)', r'ßßß\1', self.vyjimky)
            text = textlib.replaceExcept(text, r'(\]{1,2})', r'\1ßßß', self.vyjimky)
            text = textlib.replaceExcept(text, r'\{\|', r'ßßß{|', self.vyjimky)
            text = textlib.replaceExcept(text, r'\|\}([^\}])', r'|}ßßß\1', self.vyjimky)
            text = textlib.replaceExcept(text, r'\<', r'ßßß<', self.vyjimky)
            text = textlib.replaceExcept(text, r'\>', r'>ßßß', self.vyjimky)
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
                        self.seznam += '# ' + self.current_page.title(asLink=True) + '\t' + blockTemplate[-1] + '\t' + '; '.join(nalezene) + '\n'

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

        ################################################################


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
        bot = BasicBot(gen, step=1, **options)
        bot.run()
        bot2 = BasicBot(bot.gen2, step=2, **options)
        bot2.run()
        bot3 = BasicBot(bot.gen3, step=3, **options)
        bot3.run()
        page = pywikibot.Page(pywikibot.Site('cs'), 'Wikipedie:Údržbové seznamy/Nepojmenované parametry infoboxů/seznam')
        page.text = bot3.seznam.strip()
        page.save(summary=bot3.getOption('summary') if bot3.getOption('summary') else 'Robot: aktualizace')
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False


if __name__ == '__main__':
    main()
