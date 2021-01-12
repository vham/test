from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    ''' Crea nuevo usuarios '''
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    ''' Crea un nuevo usuario para token '''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    ''' Administracion del perfil de usuario '''
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        ''' toma y devuelve usuario '''
        return self.request.user
