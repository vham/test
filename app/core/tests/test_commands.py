from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_esperar_por_db_lista(self):
        ''' Prueba espera por db este lista '''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.return_value = True
            call_command('wait_for_db')

            self.assertEqual(getitem.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_espera_por_db(self, ts):
        ''' Prueba espera por db '''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            self.assertEqual(getitem.call_count, 6)
