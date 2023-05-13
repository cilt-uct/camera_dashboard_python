import unittest.mock
import jobs.data_access_layer
from .test_helper import venue_with_single_item, venue_with_items


class TestSync(unittest.TestCase):
    @unittest.mock.patch('jobs.data_access_layer.create')
    def test_create_venue_one_item(self, create):
        jobs.data_access_layer.create_venue(venue_with_single_item)
        self.assertEqual(0, create.call_count)

    @unittest.mock.patch('jobs.data_access_layer.create')
    def test_create_venue_items(self, create):
        jobs.data_access_layer.create_venue(venue_with_items)
        self.assertEqual(1, create.call_count)


if __name__ == '__main__':
    unittest.main()