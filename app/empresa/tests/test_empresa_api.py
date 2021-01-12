from faker import Faker

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Empresa

from empresa.serializers import EmpresaSerializer

fake = Faker()

EMPRESAS_URL = reverse('empresa:empresa-list')


class PublicEmpresasApiTests(TestCase):
    ''' Prueba el accesso publico a empresas API '''

    def setUp(self):
        self.client = APIClient()

    def test_login_requerido(self):
        ''' Prueba ingreso requerido para acceder listado de empresas '''
        res = self.client.get(EMPRESAS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEmpresasApiTests(TestCase):
    ''' Prueba el accesso privado a empresas API '''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='rpparada@gmail.com',
            password='testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_obtener_listado(self):
        ''' Obtener lista de empresas '''
        Empresa.objects.create(user=self.user, name='enviame')
        Empresa.objects.create(user=self.user, name='cornershop')

        res = self.client.get(EMPRESAS_URL)

        empresas = Empresa.objects.all().order_by('name')
        serializer = EmpresaSerializer(empresas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_empresas_solo_usuario(self):
        ''' Listado de empresa solo del usuario '''
        user2 = get_user_model().objects.create_user(
            email=fake.email(),
            password='testpassword'
        )
        Empresa.objects.create(user=user2, name=fake.company())
        empresa = Empresa.objects.create(user=self.user, name=fake.company())

        res = self.client.get(EMPRESAS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], empresa.name)

    def test_crear_empresa(self):
        ''' Prueba la creacion de empresas '''
        payload = {
            'name': fake.company()
        }
        self.client.post(EMPRESAS_URL, payload)
        exists = Empresa.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_crear_empresa_invalida(self):
        ''' Crear una nueva empresa invalida '''
        payload = {
            'name': ''
        }

        res = self.client.post(EMPRESAS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
