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

    def __init__(self, generator, **kwargs):
        """
        Initializer.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        # Add your own options to the bot and set their defaults
        # -always option is predefined by BaseBot class
        self.available_options.update({
            'replace': False,  # delete old text and write the new text
            'summary': None,  # your own bot summary
            'text': 'Test',  # add this text from option. 'Test' is default
            'top': False,  # append text on top of the page
            'ref': None,
        })

        ################################################################
        #                           výjimky                            #
        ################################################################

        # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
        self.vyjimky = ['nowiki']

        ################################################################
        #                           shrnutí                            #
        ################################################################

        #self.shrnuti = ''
        self.pocty = {}

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
        part of self.available_options.

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

        text = textlib.replaceExcept(text, r'\{\{', r'ßßß{{', self.vyjimky)
        text = textlib.replaceExcept(text, r'\}\}', r'}}ßßß', self.vyjimky)
        text = textlib.replaceExcept(text, r'(\[+)', r'ßßß\1', self.vyjimky)
        text = textlib.replaceExcept(text, r'(\]{1,2})', r'\1ßßß', self.vyjimky)
        text = textlib.replaceExcept(text, r'\{\|', r'ßßß{|', self.vyjimky)
        text = textlib.replaceExcept(text, r'\|\}([^\}])', r'|}ßßß\1', self.vyjimky)
        text = textlib.replaceExcept(text, r'\<', r'ßßß<', self.vyjimky)
        text = textlib.replaceExcept(text, r'\>', r'>ßßß', self.vyjimky)
        pageParts = text.strip('ß').split('ßßß')
        #newPageParts = []
        inTemplate = [0]
        inLink = [False]
        inTable = [False]
        inTag = [False]
        for part in pageParts:
            name = self.opt.ref
            if re.match(r'[Šš]ablona:', name):
                name = name[8:]
            name = re.escape(name)
            name = name.replace(r'\ ', r'[ _]')
            name = r'\{\{\s*[' + name[0].upper() + name[0].lower() + r']' + name[1:]
            if re.match(name, part):
                inTemplate.append(2)
                # part = textlib.replaceExcept(part, r'', r'', self.vyjimky)
            elif part[:2] == '{{':
                inTemplate.append(1)
            elif part[:1] == '[':
                inLink.append(True)
            elif part[:2] == '{|':
                inTable.append(True)
            elif part[:1] == '<':
                inTag.append(True)

            if inTemplate[-1] == 2 and not inLink[-1] and not inTable[-1] and not inTag[-1]:
                #part = textlib.replaceExcept(part, r'\|\s*[A-ZŽŠČŘĎŤŇÁÉÍÓÚŮÝĚ]', lambda x: x.group(0).lower(), self.vyjimky)
                #part = textlib.replaceExcept(part, r'\|[^\|\=]+?=', lambda x: x.group(0).replace('_',' '), self.vyjimky)
                ################################################################
                #                            regexy                            #
                ################################################################

                # self.opt.parametr
                # self.current_page.title()
                # with open('soubor.txt', 'a') as soubor:
                #     soubor.write('# ' + self.current_page.title(as_link=True) + '\n')
                # part = textlib.replaceExcept(part, r'', r'', self.vyjimky)
                params = re.findall(r'\|\s*([^\=\|\}]+)\s*=\s*([^\|\}]*)', part)
                for param, val in params:
                    if part.endswith(val) or val.strip():
                        param = param.strip()
                        if param in self.pocty:
                            self.pocty[param] = self.pocty[param] + 1
                        else:
                            self.pocty[param] = 1

                ################################################################
            #newPageParts.append(part)

            if part[-2:] == '}}' and inTemplate[-1] > 0:
                inTemplate.pop()
            elif part[-1:] == ']' and inLink[-1]:
                inLink.pop()
            elif part[-2:] == '|}' and inTable[-1]:
                inTable.pop()
            elif part[-1:] == '>' and inTag[-1]:
                inTag.pop()
        #text = ''.join(newPageParts)

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
        if gen_factory.handle_arg(arg) and not arg.startswith('-ref:'):
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
        for key, value in sorted(bot.pocty.items(), key=lambda kv: kv[1], reverse=True):
            print("%s: %s" % (key, value))
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False


if __name__ == '__main__':
    main()
