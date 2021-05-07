"""Tests for the patrol script."""
#
# (C) Pywikibot team, 2015-2021
#
# Distributed under the terms of the MIT license.
#
from contextlib import suppress

from scripts.patrol import PatrolBot
from tests.aspects import DefaultDrySiteTestCase, require_modules, unittest


DUMMY_PAGE_TUPLES = """
This is some text above the entries:

== Header ==
* [[User:Test 1]]: [[Page 1]], [[Page 2]]
* [[User:Test_2]]: [[Page 2]], [[Page 4]], [[Page 6]]

== Others ==
* [[User:Prefixed]]: [[Special:PrefixIndex/Page 1]],
                     [[Special:PREFIXINDEX/Page 2]]

== More test 1 ==
* [[User:Test_1]]: [[Page 3]]
"""


@require_modules('mwparserfromhell')
class TestPatrolBot(DefaultDrySiteTestCase):

    """Test the PatrolBot class."""

    def setUp(self):
        """Create a bot dummy instance."""
        super().setUp()
        self.bot = PatrolBot(self.site)

    def test_parse_page_tuples(self):
        """Test parsing the page tuples from a dummy text."""
        tuples = self.bot.parse_page_tuples(DUMMY_PAGE_TUPLES)
        for gen_user in (1, 2):
            user = 'Test {}'.format(gen_user)
            self.assertIn(user, tuples)
            self.assertEqual(tuples[user], {'Page {}'.format(i * gen_user)
                                            for i in range(1, 4)})
        self.assertIn('Prefixed', tuples)
        self.assertEqual(tuples['Prefixed'], {'Page 1', 'Page 2'})
        self.assertEqual(self.bot.parse_page_tuples('[[link]]'), {})

    def test_in_list(self):
        """Test the method which returns whether a page is in the set."""
        # Return True if there is an exact match
        self.assertTrue(self.bot.in_list({'Foo', 'Foobar'}, 'Foo'))
        self.assertTrue(self.bot.in_list({'Foo', 'Foobar'}, 'Foobar'))
        self.assertFalse(self.bot.in_list({'Foo', 'Foobar'}, 'Bar'))

        # Return True if an entry starts with the title if there is no
        # exact match
        self.assertTrue(self.bot.in_list({'Foo', 'Foobar'}, 'Foob'))
        self.assertTrue(self.bot.in_list({'Foo', 'Foobar'}, 'Foobarz'))
        self.assertTrue(self.bot.in_list({'Foo', 'Foobar', 'Bar'}, 'Barz'))
        self.assertFalse(self.bot.in_list({'Foobar', 'Bar'}, 'Foo'))

        # '' returns True if there is no exact match
        self.assertTrue(self.bot.in_list({''}, 'Foo'))
        self.assertTrue(self.bot.in_list({'', 'Foobar'}, 'Foo'))
        self.assertTrue(self.bot.in_list({'', 'Foo'}, 'Foo'))


if __name__ == '__main__':  # pragma: no cover
    with suppress(SystemExit):
        unittest.main()
