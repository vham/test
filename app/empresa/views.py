from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Empresa

from empresa import serializers


# Create your views here.
class EmpresaViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    ''' Administra empresas en db '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Empresa.objects.all()
    serializer_class = serializers.EmpresaSerializer

    def get_queryset(self):
        ''' Retorna solo las empresas del usuario '''
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        ''' Crea una nueva empresa '''
        serializer.save(user=self.request.user)
