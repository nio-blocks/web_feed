WebFeed
=======
Polls web feeds for posts.

Properties
----------
- **feed_urls**: URLs of feeds to poll.
- **get_updates**: When True, an attempt is made to output a signal when a post is updated.
- **include_query**: Whether to include queries in request to URLs.
- **lookback**: On block start, look back this amount of time to grab old posts.
- **polling_interval**: How often API is polled. When using more than one query. Each query will be polled at a period equal to the *polling interval* times the number of queries.
- **queries**: Queries to include on request to API.
- **retry_interval**: When a url request fails, how long to wait before attempting to try again.
- **retry_limit**: Number of times to retry on a poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: Creates a new signal for each Feed Post. Every field on the feed post will become a signal attribute. [feedparser](https://pythonhosted.org/feedparser/index.html) has documentation on what fields can be expected from [rss](https://pythonhosted.org/feedparser/common-rss-elements.html) and [atom](https://pythonhosted.org/feedparser/common-atom-elements.html) feeds. Feed fields will be prepended with `feed_`. The attribute `updated` will be set even if the feed format does not have it (ex. for rss feeds `updated` is set to `pubDate`.

Commands
--------
None

Dependencies
------------
-   [feedparser](https://pypi.python.org/pypi/feedparser)
-   [RESTPolling Block](https://github.com/nio-blocks/http_blocks/blob/master/rest/rest_block.py)

Output Example
--------------
The following is a list of commonly include attributes, but note that not all will be included on every signal:
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

