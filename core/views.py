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
    serializer_class = ClienteSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {'nome': ['icontains'], 'numero_documento': ['icontains']}
    search_fields = ['nome__icontains', 'numero_documento__icontains']

    def get_queryset(self):
        queryset = Cliente.objects.filter(excluido=False)  
        nome = self.request.query_params.get('nome')
        numero_documento = self.request.query_params.get('numero_documento')
        

        if nome is not None:
            queryset = queryset.filter(excluido=False, nome__icontains=nome)
        
        if numero_documento is not None :
            queryset = queryset.filter(excluido=False, numero_documento__icontains=numero_documento)
            
        queryset = queryset.order_by('nome', 'numero_documento')
        return queryset


class EquipamentoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Equipamento.objects.filter(excluido=False)
    serializer_class = EquipamentoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend,  filters.OrderingFilter]
    filterset_fields = ["id", "categoria"]
    ordering = ["id"]


class VeiculoViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = VeiculoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {'marca_modelo': ['icontains'], 'id': ['icontains']}
    search_fields = ['marca_modelo__icontains', 'id__icontains']

    def get_queryset(self):
        queryset = Veiculo.objects.filter(excluido=False)  
        marca_modelo = self.request.query_params.get('marca_modelo')
        id = self.request.query_params.get('id')
        
        if marca_modelo is not None:
            queryset = queryset.filter(excluido=False, marca_modelo__icontains=marca_modelo)
       
        if id is not None:
            queryset = queryset.filter(excluido=False, id__icontains=id)
            
        queryset = queryset.order_by('marca_modelo', 'id')
        return queryset

    
class FuncionarioViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = FuncionarioSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {'nome': ['icontains'], 'numero_documento': ['icontains']}
    search_fields = ['nome__icontains', 'numero_documento__icontains']

    def get_queryset(self):
        queryset = Funcionario.objects.filter(excluido=False)  
        nome = self.request.query_params.get('nome')
        numero_documento = self.request.query_params.get('numero_documento')
        
        if nome is not None:
            queryset = queryset.filter(excluido=False, nome__icontains=nome)
        
        if numero_documento is not None :
            queryset = queryset.filter(excluido=False, numero_documento__icontains=numero_documento)
            
        queryset = queryset.order_by('nome', 'numero_documento')
        return queryset


class ItemServicoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = ItemServico.objects.all()
    serializer_class = ItemServicoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [DjangoModelPermissions]
    ordering = ["id"]


class ServicoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["veiculo__categoria"]
    ordering = ["id"]


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

    def create_contrato(self, request, *args, **kwargs):
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
