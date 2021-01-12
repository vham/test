from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='rpparada@gmail.com', password='testpassword'):
    ''' Crea un usuario de prueba '''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_crear_usuario_solo_email(self):
        ''' Prueba creacion de usuario solo con email'''
        email = 'rpparada@gmail.com'
        password = 'rpparadapassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_nuevo_usuario_normalizacion_email(self):
        ''' Prueba normalizacion de emails en nuevos usuarios '''
        email = 'rpparada@GMAIL.COM'
        password = 'rpparadapassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_nuevo_usuario_email_invalido(self):
        ''' Prueba nuevo usuario sin email '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'rpparadapassword')

    def test_crear_nuevo_superusuario(self):
        ''' Prueba creacion de nuevo super usuario '''
        email = 'rpparada@gmail.com'
        password = 'rpparadapassword'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_empresa_str(self):
        ''' Prueba las representacion de empresa '''
        empresa = models.Empresa.objects.create(
            user=sample_user(),
            name='Enviame'
        )

        self.assertEqual(str(empresa), empresa.name)
