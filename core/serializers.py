from django.core import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from core.models import *



class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"


class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = "__all__"


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = "__all__"


class ItemServicoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ItemServico
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = "__all__"


class ServicoSerializer(FlexFieldsModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario.nome', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    itens_servico = ItemServicoSerializer(many=True, read_only=True, source='itens')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        itens_servico = instance.itens.all()
        descricao_itens = ";".join([item.descricao for item in itens_servico])
        representation['itens_servico'] = descricao_itens

        if instance.veiculo:
            representation['categoria'] = instance.veiculo.categoria
            representation['marca_modelo'] = instance.veiculo.marca_modelo
        elif instance.equipamento:
            representation['categoria'] = instance.equipamento.categoria
            representation['marca_modelo'] = instance.equipamento.marca_modelo
        else:
            representation['categoria'] = None
            representation['marca_modelo'] = None
        return representation

    class Meta:
        model = Servico
        fields = "__all__"

        expandable_fields = {
            "veiculo": VeiculoSerializer,
            "equipamento": EquipamentoSerializer,
            "usuario": UserSerializer,
        }


class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'
