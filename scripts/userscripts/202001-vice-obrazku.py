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

        shrnuti = 'počeštění šablony Více obrázků'
        self.shrnuti = self.getOption('summary') or 'Robot: ' + shrnuti

        ################################################################
        #                           infobox                            #
        ################################################################

        infobox = self.getOption('ref')
        if re.match(r'[Šš]ablona:', infobox):
            infobox = infobox[8:]
        infobox = re.escape(infobox)
        infobox = infobox.replace(r'\ ', r'[ _]')
        self.infobox = r'\{\{\s*[' + infobox[0].upper() + infobox[0].lower() + r']' + infobox[1:]

        ################################################################

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

        inBlockTemplate = [False]
        inInlineTemplate = [False]
        inLink = [False]
        inTable = [False]
        inTag = [False]
        newPageParts = []

        for part in pageParts:
            if re.match(self.infobox, part):
                inBlockTemplate.append(True)
                #part = textlib.replaceExcept(part, self.infobox, r'{{Více obrázků', self.vyjimky)
            elif part[:2] == '{{':
                inInlineTemplate.append(True)
            elif part[:1] == '[':
                inLink.append(True)
            elif part[:2] == '{|':
                inTable.append(True)
            elif part[:1] == '<':
                inTag.append(True)

            if inBlockTemplate[-1] and not inInlineTemplate[-1] and not inLink[-1] and not inTable[-1] and not inTag[-1]:
                # part = textlib.replaceExcept(part, r'\|\s*[A-ZŽŠČŘĎŤŇÁÉÍÓÚŮÝĚ]', lambda x: x.group(0).lower(), self.vyjimky)
                part = textlib.replaceExcept(part, r'\|[^\|\=]+?=', lambda x: x.group(0).replace('_',' '), self.vyjimky)
                ################################################################
                #                            změny                             #
                ################################################################

                # self.getOption('parametr')
                # self.current_page.title()
                # with open('soubor.txt', 'a') as soubor:
                #     soubor.write('# ' + self.current_page.title(asLink=True) + '\n')
                part = textlib.replaceExcept(part, r'\|\s*[^\=]*\s*=\s*(?=\||\})', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*(?:(?:header|footer|caption) |)align\s*=\s*left\/right\/center\s*', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*direction\s*=\s*horizontal\/vertical\s*', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*image(\d)\s*=', r'| obrázek\1 =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*caption(\d)\s*=', r'| popisek\1 =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*width(\d)\s*=', r'| velikost obrázku\1 =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*align\s*=', r'| zarovnání =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*direction\s*=', r'| orientace =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*width\s*=', r'| velikost obrázků =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*header\s*=', r'| hlavička =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*footer\s*=', r'| patička =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*header align\s*=', r'| zarovnání hlavičky =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*footer align\s*=', r'| zarovnání patičky =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*caption align\s*=', r'| zarovnání popisků =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*header background\s*=', r'| pozadí hlavičky =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*footer background\s*=', r'| pozadí patičky =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*background color\s*=', r'| pozadí =', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*image border\s*=', r'| rámeček obrázků =', self.vyjimky)

                part = textlib.replaceExcept(part, r'\|\s*(velikost obrázku\d|velikost obrázků)\s*=\s*(\d+)(?= *[^\dp ])', r'| \1 = \2px', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*rámeček obrázků\s*=\s*(?:[^\sn]|n[^eo])[^\|\}]*', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*rámeček obrázků\s*=\s*no', r'| rámeček obrázků = ne', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*orientace\s*=\s*(?:[^\svs]|s[^v]|sv[^i]|svi[^s]|svis[^l]|svisl[^e]|v[^e]|ve[^r]|ver[^t]|vert[^i]|verti[^c]|vertic[^a]|vertica[^l])[^\|\}]*', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*orientace\s*=\s*vertical', r'| orientace = svisle', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*(zarovnání(?: (?:hlavičky|patičky|popisků)|))\s*=\s*left', r'| \1 = vlevo', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*(zarovnání(?: (?:hlavičky|patičky|popisků)|))\s*=\s*right', r'| \1 = vpravo', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*(zarovnání(?: (?:hlavičky|patičky|popisků)|))\s*=\s*center', r'| \1 = střed', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*zarovnání\s*=\s*vpravo\s*', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*zarovnání hlavičky\s*=\s*střed\s*', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*zarovnání patičkys\s*=\s*vlevo\s*', r'', self.vyjimky)
                part = textlib.replaceExcept(part, r'\|\s*zarovnání popisků\s*=\s*vlevo\s*', r'', self.vyjimky)

                ################################################################
            newPageParts.append(part)

            if part[-2:] == '}}' and (inBlockTemplate[-1] or inInlineTemplate[-1]):
                if inBlockTemplate[-1] and inInlineTemplate[-1]:
                    inInlineTemplate.pop()
                elif inInlineTemplate[-1] and not inBlockTemplate[-1]:
                    inInlineTemplate.pop()
                elif inBlockTemplate[-1] and not inInlineTemplate[-1]:
                    inBlockTemplate.pop()
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
