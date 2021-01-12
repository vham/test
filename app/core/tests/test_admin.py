from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='rpparada@gmail.com',
            password='rpparadapassword'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='rpparada@hotmail.com',
            password='rpparadapassword',
            name='Rodrigo Parada'
        )

    def test_lista_usuarios(self):
        ''' Prueba usuarios listados en la pagina de usuarios '''
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_usuario_actualiza_informacion(self):
        ''' Usuario actualiza informacion en pagina de administracion '''
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_crear_usuario(self):
        ''' Prueba creacion de usuario desde admin '''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
