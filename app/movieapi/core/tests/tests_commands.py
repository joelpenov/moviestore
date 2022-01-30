from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def setUp(self):
        self.CALL_COMMAND = "wait_for_db"
        self.GET_CONNECTION = "django.db.utils.ConnectionHandler.__getitem__"

    def test_wait_for_db_ready(self):
        with patch(self.GET_CONNECTION) as gi:
            gi.return_value = True
            call_command(self.CALL_COMMAND)
            self.assertEqual(gi.call_count, 1)
    
    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        with patch(self.GET_CONNECTION) as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command(self.CALL_COMMAND)
            self.assertEqual(gi.call_count, 6)
