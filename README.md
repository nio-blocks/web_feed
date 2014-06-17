web_feed
========

A Block that reads RSS and Atom feeds.

This block makes uses of the python library feedparser and works for many web feed formats (i.e. Atom, RSS, etc...)

Dependencies
------------
feedparser

Every time the feed is polled, no posts older than the last "updated" time will be grabbed. For RSS feeds, "updated" likely refers to the "pubDate" of the item.

get updates
-----------
When "get updates" is set to False, an attempt will be made to keep trade of the post ids and to not grab a post again if it is updated and therefore has a new "updated" time. For RSS feeds, "id" refers to "guid".

lookback
--------
On block start, past feeds will be grabbed as far back as the lookback parameter.
