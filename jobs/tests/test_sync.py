import unittest.mock
import jobs.sync_agents


class TestSync(unittest.TestCase):

    @unittest.mock.patch('jobs.sync_agents.delete_venues')
    @unittest.mock.patch('jobs.sync_agents.create_venue')
    def test_do_sync(self, *_):
        jobs.sync_agents.do_sync()


if __name__ == '__main__':
    unittest.main()
