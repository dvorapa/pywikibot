#
# (C) Pywikibot team, 2026
#
# Distributed under the terms of the MIT license.
#
"""Unit tests for Page.stable_revision."""
from __future__ import annotations

import unittest
from contextlib import suppress
from unittest.mock import MagicMock, patch

import pywikibot
from pywikibot.exceptions import UnknownExtensionError
from pywikibot.page import Revision
from tests.aspects import TestCase


class TestPageStableRevision(TestCase):

    """Test Page.stable_revision with full mocking."""

    family = 'wikipedia'
    code = 'fi'
    dry = True

    def setUp(self) -> None:
        """Test setup."""
        super().setUp()
        self.page = pywikibot.Page(self.site, 'TestPage')
        self.page.exists = MagicMock(return_value=True)

    def _mock_response(self, data: dict | list[dict]) -> dict:
        """Helper: build API response for action=query&prop=flagged."""
        return {
            'query': {
                'pages': data if isinstance(data, list) else [data]
            }
        }

    @patch('pywikibot.site._apisite.APISite.has_extension')
    def test_stable_revision_flaggedrevs_disabled(self, mock_has_ext):
        """FlaggedRevs not enabled → return None."""
        mock_has_ext.return_value = False

        with self.assertRaisesRegex(
            UnknownExtensionError,
            'Method "stable_revid" is not implemented without the extension '
            'FlaggedRevs'
        ):
            self.page.stable_revision

    @patch('pywikibot.site._apisite.APISite.simple_request')
    @patch('pywikibot.site._apisite.APISite.has_extension')
    def test_stable_revision_no_flagged_data(self, mock_has_ext, mock_req):
        """API returns no 'flagged' key → return None."""
        mock_has_ext.return_value = True
        mock_req.return_value.submit.return_value = self._mock_response(
            {'pageid': 1, 'ns': 0, 'title': 'TestPage'}
        )

        result = self.page.stable_revision
        self.assertIsNone(result)

    @patch('pywikibot.site._apisite.APISite.simple_request')
    @patch('pywikibot.site._apisite.APISite.has_extension')
    def test_stable_revision_no_stable_revid(self, mock_has_ext, mock_req):
        """'flagged' exists but no 'stable_revid' → return None."""
        mock_has_ext.return_value = True
        mock_req.return_value.submit.return_value = self._mock_response(
            {
                'pageid': 1,
                'title': 'TestPage',
                'flagged': {'level': 1}
            }
        )

        result = self.page.stable_revision
        self.assertIsNone(result)

    @patch('pywikibot.site._apisite.APISite.simple_request')
    @patch('pywikibot.site._apisite.APISite.has_extension')
    def test_stable_revision_success(self, mock_has_ext, mock_req):
        """Valid stable_revid → return Revision with content."""
        mock_has_ext.return_value = True

        # Mock get_revision to return a real-looking Revision
        mock_rev = MagicMock(spec=Revision)
        mock_rev.revid = 12345
        mock_rev.text = 'Stable content'
        mock_rev.user = 'Reviewer'
        mock_rev.timestamp = pywikibot.Timestamp(2025, 1, 1)

        with patch.object(self.page,
                          'get_revision',
                          return_value=mock_rev):
            mock_req.return_value.submit.return_value = self._mock_response(
                {
                    'pageid': 1,
                    'title': 'TestPage',
                    'flagged': {
                        'stable_revid': 12345,
                        'level': 2,
                        'pending_since': '2025-01-01T00:00:00Z'
                    }
                }
            )

            result = self.page.stable_revision

            self.assertEqual(result, mock_rev)
            self.assertEqual(result.revid, 12345)
            self.assertIn('Stable content', result.text)

    @patch('pywikibot.site._apisite.APISite.simple_request')
    @patch('pywikibot.site._apisite.APISite.has_extension')
    def test_stable_revision_multiple_pages(self, mock_has_ext, mock_req):
        """Multiple pages in response → still find correct one."""
        mock_has_ext.return_value = True

        # Mock get_revision to return a Revision with revid=999
        mock_rev = MagicMock(spec=Revision)
        mock_rev.revid = 999
        mock_rev.text = 'Other stable content'

        with patch.object(self.page, 'get_revision', return_value=mock_rev):
            mock_req.return_value.submit.return_value = self._mock_response([
                {
                    'pageid': 1,
                    'title': 'TestPage',
                    'flagged': {'stable_revid': 999}
                },
                {
                    'pageid': 2,
                    'title': 'OtherPage',
                    'flagged': {'stable_revid': 888}
                }
            ])

            result = self.page.stable_revision
            self.assertEqual(result.revid, 999)


if __name__ == '__main__':
    with suppress(SystemExit):
        unittest.main()
