WebFeed
=======

Polls web feeds for posts.

Properties
--------------

-   **queries**: List of Feed URLs to get posts from.
-   **polling_interval**: How often API is polled. When using more than one query. Each query will be polled at a period equal to the `polling_interval` times the number of `queries`.
-   **retry_interval**: When a url request fails, how long to wait before attempting to try again.
-   **retry_limit**: When a url request fails, number of times to attempt a retry before giving up.
-   **lookback**: On block start, look back this amount of time to grab old posts.
-   **get_updates**: When True, an attempt is made to output a signal when a post is updated.


Dependencies
----------------

-   [feedparser](https://pypi.python.org/pypi/feedparser)
-   [RESTPolling Block](https://github.com/nio-blocks/http_blocks/blob/master/rest/rest_block.py)

Commands
----------------
None

Input
-------
None

Output
---------
Creates a new signal for each Feed Post. Every field on the feed post will become a signal attribute. [feedparser](https://pythonhosted.org/feedparser/index.html) has documentation on what fields can be expected from [rss](https://pythonhosted.org/feedparser/common-rss-elements.html) and [atom](https://pythonhosted.org/feedparser/common-atom-elements.html) feeds. Feed fields will be prepended with `feed_`. The attribute `updated` will be set even if the feed format does not have it (ex. for rss feeds `updated` is set to `pubDate`. The following is a list of commonly include attributes, but note that not all will be included on every signal:

```
{
  updated: datetime,
  id: string,
  feed_title: string, 
  title: string,
  summary: string,
  link: string
}
```
