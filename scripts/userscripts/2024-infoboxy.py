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
from pywikibot import pagegenerators
from pywikibot.bot import (
    ExistingPageBot,
    SingleSiteBot,
)
from pywikibot.textlib import replaceExcept


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

    shrnuti = ''

    ################################################################

    update_options = {
        'summary': 'Robot: ' + shrnuti,  # your own bot summary
        'ref': None,
    }

    def treat_page(self) -> None:
        """Load the given page, do some changes, and save it."""
        text = self.current_page.text
        vyjimky = self.vyjimky

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
        part2 = ''
        inLink = [0]
        inTable = [0]
        inTag = [0]
        newPageParts = []

        for part in pageParts:
            if re.match(self.infobox, part):
                # part = replaceExcept(part, self.infobox, r'', vyjimky)
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
                    # part2 = replaceExcept(part2, r'\|\s*[A-ZŽŠČŘĎŤŇÁÉÍÓÚŮÝĚ]', lambda x: x.group(0).lower(), vyjimky)
                    # part2 = replaceExcept(part2, r'\|[^\|\=]+?=', lambda x: x.group(0).replace('_',' '), vyjimky)
                    ################################################################
                    #                            změny                             #
                    ################################################################

                    # If you find out that you do not want to edit this page, just return.
                    # self.opt.parametr (nebo self.opt['parametr'])
                    # self.current_page.title()
                    # with open('soubor.txt', 'a') as soubor:
                    #     soubor.write('# ' + self.current_page.title(as_link=True) + '\n')
                    # part2 = replaceExcept(part2, r'', r'', vyjimky)
                    # part2 = replaceExcept(part2, r'\s*\|\s*\s*=[^\|\}]*(?=\s*[\|\}])', r'', vyjimky)
                    # part2 = replaceExcept(part2, r'\|\s*\s*=', r'|  =', vyjimky)

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
        self.put_current(text, summary=self.opt.summary)


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
        bot = BasicBot(generator=gen, **options)
        bot.infobox = infobox
        bot.run()  # guess what it does


if __name__ == '__main__':
    main()
