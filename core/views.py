import calendar
import json
import logging
import re
from datetime import date, datetime, timedelta

import psycopg2
import psycopg2.extras
import requests
from decouple import config
from django.conf import settings
from django.db.models import Count, Max
from django.shortcuts import redirect
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from unidecode import unidecode
from zeep import Client

from common.utils import generate_qr_code, render_pdf
from core.models import *
from core.serializers import *


logger = logging.getLogger(__name__)


class ClienteViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Cliente.objects.filter(excluido=False)
    serializer_class = ClienteSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["nome"]


class EquipamentoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Equipamento.objects.filter(excluido=False)
    serializer_class = EquipamentoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "categoria"]
    
    
    def create(self, request, *args, **kwargs):
        tipo = request.data.get('categoria', None)
        id = request.data.get('id', None)
        
        if tipo == 'veiculo':
            model_class = Veiculo
        elif tipo == 'equipamento':
            model_class = Equipamento
        else:
            return Response({"error": "Tipo inválido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = model_class.objects.get(id=id)
        except model_class.DoesNotExist:
            return Response({"error": f"{model_class.__name__} com ID {id} não encontrado"},
                            status=status.HTTP_404_NOT_FOUND)


        servico = Servico.objects.create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
        )

        return Response({"success": "Serviço criado com sucesso"}, status=status.HTTP_201_CREATED)

class VeiculoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Veiculo.objects.filter(excluido=False)
    serializer_class = VeiculoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "categoria"]

    
class FuncionarioViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["nome"]
    ordering_fields = ["nome"]
    ordering = ["nome"]


class ItemServicoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = ItemServico.objects.all()
    serializer_class = ItemServicoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [DjangoModelPermissions]


class ServicoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        "veiculo__categoria",
        "equipamento__categoria",
        "parecer",
    ]
    ordering = ["veiculo__categoria", "equipamento__categoria", "parecer"]
    
class UserViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]


class ContratoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    filterset_fields = ["cliente"]
    ordering_fields = ["cliente"]
    ordering = ["cliente"]


    def create(self, request, *args, **kwargs):
        if request.data:
            return self.documentos(request)
    
    @action(detail=False, methods=["post"], serializer_class=ContratoSerializer)
    def documentos(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = datetime.now()
        data_formatada = data.strftime("%d/%m/%Y")
        context = request.data
        

        return render_pdf(
            template_path=f"documentos/contrato.html",
            base_url=request.build_absolute_uri(),
            context=context,
            )
