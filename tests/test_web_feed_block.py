import unittest
from unittest.mock import patch, MagicMock
from requests import Response
from datetime import datetime, timedelta
from ..web_feed_block import WebFeed
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.modules.threading import sleep


class TestWebFeed(NIOBlockTestCase):

    @unittest.skip("Skipping TestWebFeed")
    def test_feed(self):
        block = WebFeed()
        self.configure_block(block, {
            "polling_interval": {
                "seconds": 2
            },
            "retry_interval": {
                "seconds": 5
            },
            "feed_url": "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom"
        })
        #TODO: finish unit test.
        block.start()
        block.stop()
