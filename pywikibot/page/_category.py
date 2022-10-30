"""Object representing a MediaWiki category page."""
#
# (C) Pywikibot team, 2008-2022
#
# Distributed under the terms of the MIT license.
#
from collections import defaultdict
from typing import Any, Optional, Union

import pywikibot
from pywikibot.backports import Generator, Iterable
from pywikibot.page._page import Page


__all__ = ('Category', )


class Category(Page):

    """A page in the Category: namespace."""

    def __init__(self, source, title: str = '', sort_key=None) -> None:
        """
        Initializer.

        All parameters are the same as for Page() Initializer.
        """
        self.sortKey = sort_key
        super().__init__(source, title, ns=14)
        if self.namespace() != 14:
            raise ValueError("'{}' is not in the category namespace!"
                             .format(self.title()))

    def aslink(self, sort_key: Optional[str] = None) -> str:
        """Return a link to place a page in this Category.

        .. warning:: Use this only to generate a "true" category link,
           not for interwikis or text links to category pages.

        **Usage:**

        >>> site = pywikibot.Site('wikipedia:test')
        >>> cat = pywikibot.Category(site, 'Foo')
        >>> cat.aslink()
        '[[Category:Foo]]'
        >>> cat = pywikibot.Category(site, 'Foo', sort_key='bar')
        >>> cat.aslink()
        '[[Category:Foo|bar]]'
        >>> cat.aslink('baz')
        '[[Category:Foo|baz]]'

        :param sort_key: The sort key for the article to be placed in this
            Category; if omitted, default sort key is used.
        """
        key = sort_key or self.sortKey
        title_with_sort_key = self.title(with_section=False)
        if key is not None:
            title_with_sort_key += '|' + key
        return f'[[{title_with_sort_key}]]'

    def subcategories(self,
                      recurse: Union[int, bool] = False,
                      total: Optional[int] = None,
                      content: bool = False):
        """
        Iterate all subcategories of the current category.

        :param recurse: if not False or 0, also iterate subcategories of
            subcategories. If an int, limit recursion to this number of
            levels. (Example: recurse=1 will iterate direct subcats and
            first-level sub-sub-cats, but no deeper.)
        :param total: iterate no more than this number of
            subcategories in total (at all levels)
        :param content: if True, retrieve the content of the current version
            of each category description page (default False)
        """

        def is_cache_valid(cache: dict, content: bool) -> bool:
            return cache['content'] or not content

        if not self.categoryinfo['subcats']:
            return

        if not isinstance(recurse, bool) and recurse:
            recurse -= 1

        if (not hasattr(self, '_subcats')
                or not is_cache_valid(self._subcats, content)):
            cache = {'data': [], 'content': content}

            for subcat in self.site.categorymembers(
                    self, member_type='subcat', total=total, content=content):
                cache['data'].append(subcat)
                yield subcat
                if total is not None:
                    total -= 1
                    if total == 0:
                        return

                if recurse:
                    for item in subcat.subcategories(
                            recurse, total=total, content=content):
                        yield item
                        if total is None:
                            continue

                        total -= 1
                        if total == 0:
                            return

            # cache is valid only if all subcategories are fetched (T88217)
            self._subcats = cache
        else:
            for subcat in self._subcats['data']:
                yield subcat
                if total is not None:
                    total -= 1
                    if total == 0:
                        return

                if recurse:
                    for item in subcat.subcategories(
                            recurse, total=total, content=content):
                        yield item
                        if total is None:
                            continue

                        total -= 1
                        if total == 0:
                            return

    def articles(self, *,
                 recurse: Union[int, bool] = False,
                 **kwargs: Any) -> Iterable[Page]:
        """
        Yield all articles in the current category.

        By default, yields all pages in the category that are not
        subcategories.

        **Usage:**

        >>> site = pywikibot.Site('wikipedia:test')
        >>> cat = pywikibot.Category(site, 'Pywikibot')
        >>> list(cat.articles())
        [Page('Pywikibot nobots test')]
        >>> for p in cat.articles(recurse=1, namespaces=2, total=3):
        ...     print(p.depth)
        ...
        2
        3
        4

        .. versionchanged:: 8.0
           all parameters are keyword arguments only.

        :param recurse: if not False or 0, also iterate articles in
            subcategories. If an int, limit recursion to this number of
            levels. (Example: ``recurse=1`` will iterate articles in
            first-level subcats, but no deeper.)
        :param kwargs: Additional parameters. Refer to
            :meth:`APISite.categorymembers()
            <pywikibot.site._generators.GeneratorsMixin.categorymembers>`
            for complete list (*member_type* excluded).
        """
        if kwargs.pop('member_type', False):
            raise TypeError(
                "articles() got an unexpected keyword argument 'member_type'")

        return self.members(
            member_type=['page', 'file'], recurse=recurse, **kwargs)

    def members(self, *,
                recurse: bool = False,
                total: Optional[int] = None,
                **kwargs: Any) -> Iterable[Page]:
        """Yield all category contents (subcats, pages, and files).

        **Usage:**

        >>> site = pywikibot.Site('wikipedia:test')
        >>> cat = pywikibot.Category(site, 'Pywikibot')
        >>> list(cat.members(member_type='subcat'))
        [Category('Category:Subpage testing')]
        >>> list(cat.members(member_type=['page', 'file']))
        [Page('Pywikibot nobots test')]

        Calling this method with ``member_type='subcat'`` is *almost*
        equal to calling :meth:`subcategories`. Calling this method with
        ``member_type=['page', 'file']`` is equal to calling
        :meth:`articles`.

        .. versionchanged:: 8.0
           all parameters are keyword arguments only. Additional
           parameters are supported.

        :param recurse: if not False or 0, also iterate articles in
            subcategories. If an int, limit recursion to this number of
            levels. (Example: ``recurse=1`` will iterate articles in
            first-level subcats, but no deeper.)
        :param total: iterate no more than this number of pages in
            total (at all levels)
        :param kwargs: Additional parameters. Refer to
            :meth:`APISite.categorymembers()
            <pywikibot.site._generators.GeneratorsMixin.categorymembers>`
            for complete list.
        """
        seen = set()
        for member in self.site.categorymembers(self, total=total, **kwargs):
            if recurse:
                seen.add(hash(member))
            yield member
            if total is not None:
                total -= 1
                if total == 0:
                    return

        if recurse:
            if not isinstance(recurse, bool) and recurse:
                recurse -= 1

            for subcat in self.subcategories():
                for member in subcat.members(
                        recurse=recurse, total=total, **kwargs):
                    hash_value = hash(member)
                    if hash_value in seen:
                        continue

                    seen.add(hash_value)
                    yield member
                    if total is None:
                        continue

                    total -= 1
                    if total == 0:
                        return

    def isEmptyCategory(self) -> bool:  # noqa: N802
        """Return True if category has no members (including subcategories)."""
        ci = self.categoryinfo
        return sum(ci[k] for k in ['files', 'pages', 'subcats']) == 0

    def isHiddenCategory(self) -> bool:  # noqa: N802
        """Return True if the category is hidden."""
        return 'hiddencat' in self.properties()

    @property
    def categoryinfo(self) -> dict:
        """
        Return a dict containing information about the category.

        The dict contains values for:

        Numbers of pages, subcategories, files, and total contents.
        """
        return self.site.categoryinfo(self)

    def newest_pages(
        self,
        total: Optional[int] = None
    ) -> Generator[Page, None, None]:
        """
        Return pages in a category ordered by the creation date.

        If two or more pages are created at the same time, the pages are
        returned in the order they were added to the category. The most
        recently added page is returned first.

        It only allows to return the pages ordered from newest to oldest, as it
        is impossible to determine the oldest page in a category without
        checking all pages. But it is possible to check the category in order
        with the newly added first and it yields all pages which were created
        after the currently checked page was added (and thus there is no page
        created after any of the cached but added before the currently
        checked).

        :param total: The total number of pages queried.
        :return: A page generator of all pages in a category ordered by the
            creation date. From newest to oldest.

            .. note:: It currently only returns Page instances and not a
               subclass of it if possible. This might change so don't
               expect to only get Page instances.
        """
        def check_cache(latest):
            """Return the cached pages in order and not more than total."""
            cached = []
            for timestamp in sorted((ts for ts in cache if ts > latest),
                                    reverse=True):
                # The complete list can be removed, it'll either yield all of
                # them, or only a portion but will skip the rest anyway
                cached += cache.pop(timestamp)[:None if total is None else
                                               total - len(cached)]
                if total and len(cached) >= total:
                    break  # already got enough
            assert total is None or len(cached) <= total, \
                'Number of caches is more than total number requested'
            return cached

        # all pages which have been checked but where created before the
        # current page was added, at some point they will be created after
        # the current page was added. It saves all pages via the creation
        # timestamp. Be prepared for multiple pages.
        cache = defaultdict(list)
        # TODO: Make site.categorymembers is usable as it returns pages
        # There is no total defined, as it's not known how many pages need to
        # be checked before the total amount of new pages was found. In worst
        # case all pages of a category need to be checked.
        for member in pywikibot.data.api.QueryGenerator(
            site=self.site, parameters={
                'list': 'categorymembers', 'cmsort': 'timestamp',
                'cmdir': 'older', 'cmprop': 'timestamp|title',
                'cmtitle': self.title()}):
            # TODO: Upcast to suitable class
            page = pywikibot.Page(self.site, member['title'])
            assert page.namespace() == member['ns'], \
                'Namespace of the page is not consistent'
            cached = check_cache(pywikibot.Timestamp.fromISOformat(
                member['timestamp']))
            yield from cached
            if total is not None:
                total -= len(cached)
                if total <= 0:
                    break
            cache[page.oldest_revision.timestamp] += [page]
        else:
            # clear cache
            assert total is None or total > 0, \
                'As many items as given in total already returned'
            yield from check_cache(pywikibot.Timestamp.min)
