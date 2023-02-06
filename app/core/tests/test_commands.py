"""
Test custom Django managment commands
"""
from unittest.mock import patch
# hendlanje erorra kada pozivamo bazu, a ona još nije spremna
from psycopg2 import OperationalError as Psycopg2Error
# helper funkcija
from django.core.management import call_command
# exception handler
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # prvih 2 puta pozovi mock metodu, da raisas error
        # onda 3 puta operationError
        # zadnji put true
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
