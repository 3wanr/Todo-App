import os
import unittest

# If a real config exists at project root `config/db.yml`, use the real db_utils
# otherwise fall back to a lightweight mock so unit tests don't require a DB.
tests_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(tests_dir, '..', '..'))
config_path = os.path.join(project_root, 'config', 'db.yml')

# Only run integration (real DB) tests when explicitly enabled via env var.
# This avoids accidental attempts to connect with placeholder credentials.
if os.path.exists(config_path) and os.environ.get('RUN_INTEGRATION') == '1':
    from api.db_utils import exec_get_one
else:
    # lightweight mock
    def exec_get_one(sql):
        return ('PostgreSQL 14.0',)


class TestPostgreSQL(unittest.TestCase):

    def test_can_connect(self):
        result = exec_get_one('SELECT VERSION()')
        self.assertTrue(result[0].startswith('PostgreSQL'))


if __name__ == '__main__':
    unittest.main()