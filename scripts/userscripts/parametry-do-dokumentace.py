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
        Constructor.

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

        # call constructor of the super class
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
                                      'pywikibot.config.simulate', 1)
            # use simulate variable instead
            pywikibot.config.simulate = True
            pywikibot.output('config.simulate was set to True')

    def treat_page(self):
        """Load the given page, do some changes, and save it."""
        text = self.current_page.text

        ################################################################
        #                           výjimky                            #
        ################################################################

        # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
        exceptions = ['comment', 'nowiki', 'source', 'code', 'pre']

        ################################################################
        #                           shrnutí                            #
        ################################################################

        shrnuti = 'vyčlenění dokumentace'

        ################################################################
        #                            regexy                            #
        ################################################################

        # self.opt.parametr
        # with open('soubor.txt', 'a') as soubor:
        #     soubor.write('# ' + self.current_page.title(as_link=True) + '\n')
        # text = textlib.replaceExcept(text, r'', r'', exceptions)
        infobox = self.current_page.title(withNamespace=False)
        kategorie = re.findall(r'\[\[ *(?:' + r'|'.join(self.current_page.site.namespaces.CATEGORY) + r') *:[^\]]+\]\]', text, flags=re.I)
        text = textlib.replaceExcept(text, r'(?i)\n?\[\[ *(?:' + r'|'.join(self.current_page.site.namespaces.CATEGORY) + r') *:[^\]]+\]\]\n?', r'\n', exceptions)
        if not re.search(r'\{\{ *(Dokumentace|Documentation) *\}\}', text, flags=re.I):
            if '<noinclude>' in text:
                text = '<noinclude>\n{{Dokumentace}}'.join(text.rsplit('<noinclude>', 1))
            else:
                text += '<noinclude>{{Dokumentace}}</noinclude>'
        parametry = str(text)
        self.put_current(text, summary='Robot: ' + (self.opt.summary if self.opt.summary else shrnuti))


        parametry = parametry.replace('{{{', '\n{{{')
        parametry = re.sub(r'(?m)^((?!\{\{\{).)*$', r'', parametry)
        parametry = re.sub(r'[<|}][^\n]*', r' = ', parametry)
        parametry = parametry.replace('{{{', ' | ')
        parametry = list(filter(None, parametry.split('\n')))
        nparametry = parametry.pop(0)
        videno = [nparametry]
        for radek in parametry:
            if radek not in videno:
                nparametry += '\n' + radek
                videno.append(radek)
        parametry = nparametry


        self.current_page = pywikibot.Page(self.current_page.site, 'Template:' + infobox + '/doc')
        text = self.current_page.text
        if not self.current_page.exists():
            preload = pywikibot.Page(pywikibot.Site('cs'), 'Šablona:Dokumentace/preload')
            text = str(preload.text)
            ocem = pywikibot.input('O čem jsou články s infoboxem?')
            if not ocem:
                ocem = 'o tématu ' + infobox.replace('Infobox - ', '').replace('Infobox ', '')
            text = text.replace('a k...', ' ve článcích ' + ocem + '.')
            
            text = text.replace('<includeonly />', '')
            regex = textlib._get_regexes(['noinclude'], self.current_page.site)[0]
            for match in re.finditer(regex, text):
                before = text[:match.start()]
                after = text[match.end():]
                text = before + after
            text = text.replace('<includeonly>subst:</includeonly>', 'subst:')
            text = '\n\kategorie\n</includeonly>'.join(text.rsplit('\n\n\n</includeonly>', 1)).replace('\kategorie', '\n'.join(kategorie))
        else:
            if '</includeonly>' in text:
                text = '\n\kategorie\n</includeonly>'.join([tag.rstrip('\n') for tag in text.rsplit('</includeonly>', 1)]).replace('\kategorie', '\n'.join(kategorie))
            else:
                text += '<includeonly>\n' + '\n'.join(kategorie) + '\n</includeonly>'


        if not any(x in text for x in ('<source', '<syntaxhighlight', '<pre', '<code')):
            text = text.replace('== Použití ==', '== Použití ==\n<source lang=moin>{{' + infobox + '\n' + parametry + '\n}}</source>')
        else:
            text = re.sub(r'\<((source|syntaxhighlight|pre|code)[^\>]*)\>\s*(\<nowiki\>)?\{(\<nowiki *\/\>)?\{(\<\/nowiki>)? *' + re.compile(infobox).pattern + r'[^\<]*?\<\/\2\>', r'<\1>{{' + infobox + r'\n' + parametry + r'\n}}</\2>', text, count=1)
            shrnuti = 'aktualizace dokumentace'
        pywikibot.output(text)
        self.put_current(text, summary='Robot: ' + (self.opt.summary if self.opt.summary else shrnuti))

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
    genFactory = pagegenerators.GeneratorFactory()

    # Parse command line arguments
    for arg in local_args:

        # Catch the pagegenerators options
        if genFactory.handle_arg(arg):
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
    gen = genFactory.getCombinedGenerator(preload=True)
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
