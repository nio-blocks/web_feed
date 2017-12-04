import calendar
import time
from feedparser import parse

from nio.util.discovery import discoverable
from nio.signal.base import Signal
from nio.modules.scheduler import Job
from nio.properties import BoolProperty, StringProperty, TimeDeltaProperty, \
    ListProperty, PropertyHolder, VersionProperty

from .rest_polling.rest_polling_base import RESTPolling


class FeedEntrySignal(Signal):
    def __init__(self, entry, feed):
        super().__init__()
        for k in entry:
            setattr(self, k, entry[k])
        for k in feed:
            setattr(self, "feed_" + k, feed[k])
        # feedparser will give all entries an "updated" property even if
        # it doesn't exist, so make sure we save it.
        if "updated" not in entry:
            setattr(self, "updated", entry.updated)


class FeedURLField(PropertyHolder):
    feed_url = StringProperty(title='URL', default='')


@discoverable
class WebFeed(RESTPolling):
    """ A block that gets entries from a web feed.

    Attributes:
        feed_urls (List(str)): Feeds URLs to track.
        lookback (timedelta): Initial amount of time to lookback
            for old feed entries.
        get_updates (bool): Notify a signal when a feed entry is updated.

    """
    feed_urls = ListProperty(FeedURLField, title='Feeds', default=[])
    lookback = TimeDeltaProperty(
        default={"seconds": 90}, title='Lookback Period')
    get_updates = BoolProperty(default=True, title='Notify on Updates?')
    version = VersionProperty("1.0.1")

    def __init__(self):
        super().__init__()
        self._last_time = []
        self._next_last_time = []
        self._ids = []
        self._index = 0  # Used to keep track of what feed is being polled.

    def configure(self, context):
        super().configure(context)
        lookback_seconds = self.lookback().total_seconds()
        now_minus_lookback = calendar.timegm(time.gmtime()) - lookback_seconds
        for url in self.feed_urls():
            self._last_time.append(now_minus_lookback)
            self._next_last_time.append(now_minus_lookback)
            self._ids.append([])

    def poll(self, paging=False):
        """ Overriden from base class since we use feedparser
        instead of requests.
        """
        try:
            response = parse(self.feed_urls[self._index].feed_url())
            entries = response.entries
            fresh_entries = self._find_fresh_entries(entries)
            signals = []
            for entry in fresh_entries:
                signals.append(self._create_signal(entry, response.feed))
            if signals:
                self.notify_signals(signals)
            # After a successful poll, set _last_time for the next poll.
            self._last_time[self._index] = self._next_last_time[self._index]
            self._next_feed()
            # Reset polling if it was cleared due to a retry.
            self._poll_job = self._poll_job or Job(
                self.poll,
                self.polling_interval,
                True
            )
        except Exception as e:
            self.logger.error("Error when polling feed: {0}".format(e))
            # If there was an error, reset _next_last_time
            self._next_last_time[self._index] = self._last_time[self._index]
            self._retry_poll(paging=False)

    def _find_fresh_entries(self, entries):
        """Filter down entries to only fresh entries."""
        fresh_entries = [e for e in entries
                         if self._get_entry_time(e) >
                         self._last_time[self._index]]
        # Filter out repeat ids if not getting updates.
        if not self.get_updates():
            fresh_entries = [e for e in fresh_entries
                             if not e.get('id') or
                             e.get('id') not in self._ids[self._index]]
            new_ids = [e.get('id') for e in entries]
            self._ids[self._index] = new_ids
        return fresh_entries

    def _get_entry_time(self, entry):
        # If entry does not have an updated time, then consider it 'now'.
        seconds_from_epoch = calendar.timegm(time.gmtime())
        try:
            seconds_from_epoch = calendar.timegm(entry["updated_parsed"])
            # Update _next_last_time when we get a more recent entry.
            if seconds_from_epoch > self._next_last_time[self._index]:
                self._next_last_time[self._index] = seconds_from_epoch
        except:
            self.logger.warning("Entry's updated time is not available")
        return seconds_from_epoch

    def _create_signal(self, entry, feed):
        return FeedEntrySignal(entry, feed)

    def _next_feed(self):
        self._index += 1
        if self._index >= len(self.feed_urls()):
            self._index = 0
