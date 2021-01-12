import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    ''' Comando django para detener ejecucion mientras db esta desabilitada '''

    def handle(self, *args, **options):
        self.stdout.write('Esperando por db ...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(
                    'Base de Datos no diponible, esperando 1 segundo ...'
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Base de Datos disponible!!'))
