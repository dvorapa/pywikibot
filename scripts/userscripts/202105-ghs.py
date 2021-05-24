#!/usr/bin/python
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

All settings can be made either by giving option with the command line
or with a settings file which is scripts.ini by default. If you don't
want the default values you can add any option you want to change to
that settings file below the [basic] section like:

    [basic] ; inline comments starts with colon
    # This is a commend line. Assignments may be done with '=' or ':'
    text: A text with line break and
        continuing on next line to be put
    replace: yes ; yes/no, on/off, true/false and 1/0 is also valid
    summary = Bot: My first test edit with pywikibot

Every script has its own section with the script name as header.

In addition the following generators and filters are supported but
cannot be set by settings file:

&params;
"""
#
# (C) Pywikibot team, 2006-2021
#
# Distributed under the terms of the MIT license.
#
import pywikibot, re
from pywikibot import pagegenerators
from pywikibot.backports import Tuple
from pywikibot.bot import (
    ConfigParserBot,
    ExistingPageBot,
    NoRedirectPageBot,
    SingleSiteBot,
)
from pywikibot.exceptions import NoPageError
from pywikibot.textlib import replaceExcept
from datetime import date
from pathlib import Path
from requests import get
from time import sleep


# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {'&params;': pagegenerators.parameterHelp}  # noqa: N816


class BasicBot(
    # Refer pywikobot.bot for generic bot classes
    SingleSiteBot,  # A bot only working on one site
    ConfigParserBot,  # A bot which reads options from scripts.ini setting file
    # CurrentPageBot,  # Sets 'current_page'. Process it in treat_page method.
    #                  # Not needed here because we have subclasses
    ExistingPageBot,  # CurrentPageBot which only treats existing pages
    NoRedirectPageBot,  # CurrentPageBot which only treats non-redirects
):

    """
    An incomplete sample bot.
    """

    def __init__(self, generator, **kwargs) -> None:
        """
        Initializer.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        # Add your own options to the bot and set their defaults
        # -always option is predefined by BaseBot class
        self.available_options.update({
            'summary': None,  # your own bot summary
            'ref': None,
        })

        # call initializer of the super class
        super().__init__(site=True, **kwargs)

        ################################################################
        #                           výjimky                            #
        ################################################################

        # ['comment', 'header', 'pre', 'source', 'score', 'ref', 'template', 'startspace', 'table', 'hyperlink', 'gallery', 'link', 'interwiki', 'property', 'invoke', 'category', 'file', 'pagelist'] + libovolný HTML prvek
        self.vyjimky = tuple()

        ################################################################
        #                           shrnutí                            #
        ################################################################

        shrnuti = 'aktualizace symbolů nebezpečí GHS z PubChem'

        ################################################################

        self.ensite = pywikibot.Site('en')
        self.date = date.today().isoformat()
        self.running = False
        self.last = pywikibot.Page(self.site, 'Fluoren')

        ################################################################

        self.shrnuti = self.opt.summary or 'Robot: ' + shrnuti

        infobox = self.opt.ref or 'Šablona:Infobox - chemická sloučenina'
        if re.match(r'[Šš]ablona:', infobox):
            infobox = infobox[8:]
        infobox = re.escape(infobox)
        infobox = infobox.replace(r'\ ', r'[ _]')
        self.infobox = r'\{\{\s*[' + infobox[0].upper() + infobox[0].lower() + r']' + infobox[1:] + '(?=\s*[\|\}\<])'

        # assign the generator to the bot
        self.generator = generator

    def treat_page(self) -> None:
        """Load the given page, do some changes, and save it."""
        stranka = self.current_page
        if not self.running:
            if stranka != self.last:
                return False
            else:
                self.running = True
        elif self.running:
            self.last = stranka
        try:
            item = stranka.data_item()
        except NoPageError:
            return False

        try:
            enname = item.getSitelink(self.ensite)
            print(enname)
            sleep(5)
            cid_json = get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{enname}/JSON'.format(enname=enname)).json()
            cid = cid_json['PC_Compounds'][0]['id']['id']['cid']
        except (KeyError, NoPageError):
            cid = stranka.get_best_claim(prop='P662')
            if cid is not None:
                cid = cid._formatValue()
            else:
                try:
                    inchi = stranka.get_best_claim(prop='P234')
                    if inchi is None:
                        raise KeyError
                    sleep(5)
                    cid_json = get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchi/{inchi}/JSON'.format(inchi=inchi)).json()
                    cid = cid_json['PC_Compounds'][0]['id']['id']['cid']
                except KeyError:
                    try:
                        inchikey = stranka.get_best_claim(prop='P235')
                        if inchikey is None:
                            raise KeyError
                        sleep(5)
                        cid_json = get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchikey}/JSON'.format(inchikey=inchikey)).json()
                        cid = cid_json['PC_Compounds'][0]['id']['id']['cid']
                    except KeyError:
                        try:
                            smiles = stranka.get_best_claim(prop='P233')
                            if smiles is None:
                                raise KeyError
                            sleep(5)
                            cid_json = get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/JSON'.format(smiles=smiles)).json()
                            cid = cid_json['PC_Compounds'][0]['id']['id']['cid']
                        except KeyError:
                            return False
        print(cid)

        sleep(5)
        ghs_json = get('https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON?heading=GHS+Classification'.format(cid=cid)).json()
        try:
            ghs_list = ghs_json['Record']['Section'][0]['Section'][0]['Section'][0]['Information'][0]['Value']['StringWithMarkup'][0]['Markup']
        except KeyError:
            return False
        ghs = []
        for ghs_entry in ghs_list:
            ghs.append('{{' + Path(ghs_entry['URL']).stem + '}}')
        ghs = ''.join(sorted(ghs))
        print(ghs)

        signal = ghs_json['Record']['Section'][0]['Section'][0]['Section'][0]['Information'][1]['Value']['StringWithMarkup'][0]['String']
        if signal == 'Danger':
            signal='{{Nebezpečí}}'
        elif signal == 'Warning':
            signal='{{Varování}}'
        else:
            print('>>> Neznámé signální slovo <<<')
        print(signal)

        enname = ghs_json['Record']['RecordTitle']
        print(enname)

        text = stranka.text
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

                    # self.opt.parametr nebo self.opt['parametr']
                    # stranka.title()
                    # with open('soubor.txt', 'a') as soubor:
                    #     soubor.write('# ' + stranka.title(as_link=True) + '\n')
                    # part2 = replaceExcept(part2, r'\|\s*\s*=', r'|  =', vyjimky)
                    part2 = replaceExcept(part2, r'\|\s*symboly[ _]nebezpečí\s*=[^\|\}]*(?=\s*[\|\}])', r'', vyjimky)

                    pattern = re.compile(r'\|\s*symboly[ _]nebezpečí[ _]GHS\s*=[^\|\}]*?(?=\s*[\|\}])')
                    line = r'| symboly nebezpečí GHS = {ghs}<ref name=pubchem_cid_{cid}>{{{{Citace elektronického periodika | titul = {enname} | periodikum = pubchem.ncbi.nlm.nih.gov | vydavatel = PubChem | url = https://pubchem.ncbi.nlm.nih.gov/compound/{cid} | jazyk = en | datum přístupu = {date} }}}}</ref><br>{signal}<ref name=pubchem_cid_{cid} />'
                    line = line.format(cid=cid, enname=enname, ghs=ghs, date=self.date, signal=signal)
                    if pattern.search(part2):
                        part2 = pattern.sub(line, part2)
                    else:
                        part2 = replaceExcept(part2, r'\}\}', r' ' + line + r'\n}}', vyjimky)

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


def main(*args: Tuple[str, ...]) -> None:
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    """
    options = {}
    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    gen_factory = pagegenerators.GeneratorFactory()

    for arg in local_args:
        arg, sep, value = arg.partition(':')
        option = arg[1:]
        if option == 'ref':
            options[option] = value

    # Process pagegenerators arguments
    local_args = gen_factory.handle_args(local_args)

    # Parse your own command line arguments
    for arg in local_args:
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
    else:
        pywikibot.bot.suggest_help(missing_generator=True)


if __name__ == '__main__':
    main()
