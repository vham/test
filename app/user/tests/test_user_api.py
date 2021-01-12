from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTest(TestCase):
    ''' Prueba api usuario (publico) '''

    def setUp(self):
        self.client = APIClient()

    def test_crear_usuario_valido(self):
        ''' Prueba creacion de usuario '''
        payload = {
            'email': 'rpparada@gmail.com',
            'password': 'testpassword',
            'name': 'Rodrigo Parada'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_crear_usuario_existente(self):
        ''' Prueba usuario ya creado '''
        payload = {
            'email': 'rpparada@gmail.com',
            'password': 'testpassword',
            'name': 'Rodrigo Parada'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_muy_corto(self):
        ''' Prueba contrasena debe ser mas larga que 5 '''
        payload = {
            'email': 'rpparada@gmail.com',
            'password': 'll',
            'name': 'Rodrigo Parada'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_crear_token_usuario(self):
        ''' Prueba envio de token para usuario '''
        payload = {
            'email': 'rpparada@gmail.com',
            'password': 'll',
            'name': 'Rodrigo Parada'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_crear_token_invalido(self):
        ''' Prueba token invalido '''
        create_user(
            email='rpparada@gmail.com',
            password='testpassword'
        )
        payload = {
            'email': 'rpparada@gmail.com',
            'password': 'another',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_sinusuario(self):
        ''' Prueba token no es creado si le usuario no existe '''
        payload = {
            'email': 'rpparada@gmail.com',
            'password': 'testpassword',
            'name': 'Rodrigo Parada'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_sintoken(self):
        ''' Prueba que email y contrasena son requeridos '''
        payload = {
            'email': 'test',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_accesso_no_autorizado(self):
        ''' Prueba accesso a informacion de usuario no autorizado '''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    ''' Pruebas que requieren autentificacion '''

    def setUp(self):
        self.user = create_user(
            email='rpparada@gmail.com',
            password='testpassword',
            name='Rodrigo Parada'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_accesso_perfil(self):
        ''' Prueba accesso exitoso a perfil de usuario '''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_perfil_nopermitido(self):
        ''' Probar que no se puede hacer ports en url del perfil '''
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_actualizacion_perfil(self):
        ''' Probar actualizacion de datos de usuarios '''
        payload = {
            'name': 'nuevo name',
            'password': 'newtestpassword'
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
