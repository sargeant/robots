from robots.tests import *

class TestQueueController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='queue', action='index'))
        # Test response...
