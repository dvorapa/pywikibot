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
            'ref': None,
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

        shrnuti = 'standardizace infoboxu'

        ################################################################

        self.shrnuti = self.getOption('summary') or 'Robot: ' + shrnuti

        infobox = self.getOption('ref')
        if re.match(r'[Šš]ablona:', infobox):
            infobox = infobox[8:]
        infobox = re.escape(infobox)
        infobox = infobox.replace(r'\ ', r'[ _]')
        self.infobox = r'\{\{\s*[' + infobox[0].upper() + infobox[0].lower() + r']' + infobox[1:] + '(?=\s*[\|\}])'

        # assign the generator to the bot
        self.generator = generator

    def treat_page(self):
        """Load the given page, do some changes, and save it."""
        text = self.current_page.text

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
        part2 = ''
        inLink = [0]
        inTable = [0]
        inTag = [0]
        newPageParts = []

        for part in pageParts:
            if re.match(self.infobox, part):
                # part = textlib.replaceExcept(part, self.infobox, r'', self.vyjimky)
                inTemplate.append(2)
            elif part[:2] == '{{':
                inTemplate.append(1)
            elif part[:1] == '[':
                inLink.append(1 if inTemplate[-1] else 2)
            elif part[:2] == '{|':
                inTable.append(1 if inTemplate[-1] else 2)
            elif part[:1] == '<':
                inTag.append(1 if inTemplate[-1] else 2)

            if 2 in inTemplate:
                newPart = part
                if 1 in (inTemplate[-1], inLink[-1], inTable[-1], inTag[-1]):
                    newPart = newPart.replace('|', 'ßßß').replace('}}', 'ẞẞẞ')
                part2 += newPart
            else:
                newPageParts.append(part)

            if part[-2:] == '}}' and inTemplate[-1]:
                if inTemplate[-1] == 2:
                    part2 = textlib.replaceExcept(part2, r'\|\s*[A-ZŽŠČŘĎŤŇÁÉÍÓÚŮÝĚ]', lambda x: x.group(0).lower(), self.vyjimky)
                    part2 = textlib.replaceExcept(part2, r'\|[^\|\=]+?=', lambda x: x.group(0).replace('_',' '), self.vyjimky)
                    ################################################################
                    #                            změny                             #
                    ################################################################

                    # self.getOption('parametr')
                    # self.current_page.title()
                    # with open('soubor.txt', 'a') as soubor:
                    #     soubor.write('# ' + self.current_page.title(as_link=True) + '\n')
                    # part2 = textlib.replaceExcept(part2, r'', r'', self.vyjimky)
                    # part2 = textlib.replaceExcept(part2, r'\s*\|\s*\s*=[^\|\}]*(?=\s*[\|\}])', r'', self.vyjimky)
                    part2 = textlib.replaceExcept(part2, r'\|\s*jméno\s*=', r'| název =', self.vyjimky)
                    part2 = textlib.replaceExcept(part2, r'\|\s*založeno\s*=', r'| první ročník =', self.vyjimky)
                    part2 = textlib.replaceExcept(part2, r'\|\s*počet titulů amatérské éry\s*=', r'| nejvíce titulů amatérské éry =', self.vyjimky)
                    part2 = textlib.replaceExcept(part2, r'\|\s*počet titulů amatérské éry v řadě\s*=', r'| nejvíce titulů amatérské éry v řadě =', self.vyjimky)
                    part2 = textlib.replaceExcept(part2, r'\|\s*počet titulů otevřené éry\s*=', r'| nejvíce titulů otevřené éry =', self.vyjimky)
                    part2 = textlib.replaceExcept(part2, r'\|\s*počet titulů otevřené éry v řadě\s*=', r'| nejvíce titulů otevřené éry v řadě =', self.vyjimky)

                    ################################################################
                    newPageParts.append(part2.replace('ßßß', '|').replace('ẞẞẞ', '}}'))
                    part2 = ''
                inTemplate.pop()
            elif part[-1:] == ']' and inLink[-1]:
                inLink.pop()
            elif part[-2:] == '|}' and inTable[-1]:
                inTable.pop()
            elif part[-1:] == '>' and inTag[-1]:
                inTag.pop()

        text = ''.join(newPageParts)

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
        if gen_factory.handleArg(arg) and not arg.startswith('-ref:'):
            continue  # nothing to do here

        # Now pick up your own options
        arg, sep, value = arg.partition(':')
        option = arg[1:]
        if option in ('summary', 'text'):
            if not value:
                pywikibot.input('Please enter a value for ' + arg)
            options[option] = value
        if option == 'ref':
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
