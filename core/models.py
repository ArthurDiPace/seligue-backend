from enum import unique
from xml.etree.ElementInclude import default_loader

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models

from common import enums


class Cliente(models.Model):
    observacao = models.TextField(max_length=500, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=enums.ClienteTipo.choices())
    numero_documento = models.CharField(max_length=18)
    nome = models.CharField(max_length=80)
    data_nascimento = models.DateField(null=True, blank=True)
    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=120)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=80)
    municipio = models.CharField(max_length=80)
    uf = models.CharField(max_length=2)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, null=True, blank=True)
    excluido = models.BooleanField(default=False)
    data_cadastro = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to="pessoas_fotos", null=True, blank=True)

    def delete(self):
        self.excluido = True
        self.save()

class Veiculo(models.Model):
    placa = models.CharField(max_length=7, null=True, blank=True, default=None)
    categoria = models.CharField(
        max_length=10, choices=enums.EquipamentoCategoria.choices(), default='veiculo'
    )
    uf = models.CharField(max_length=2)
    proprietario = models.CharField(max_length=80)
    municipio = models.CharField(max_length=80)
    chassi = models.CharField(max_length=20)
    marca_modelo = models.CharField(max_length=80)
    cor = models.CharField(max_length=20)
    ano_fabricacao = models.CharField(max_length=4)
    ano_modelo = models.CharField(max_length=4)
    combustivel = models.CharField(max_length=20)
    licenciamento = models.CharField(max_length=4)
    restricoes = models.TextField(null=True, blank=True)
    odometro = models.CharField(max_length=20, null=True, blank=True)
    excluido = models.BooleanField(default=False)
    data_cadastro = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=enums.EquipamentoStatus.choices())
    observacao = models.TextField(max_length=300, blank=True, null=True)
    
    def delete(self):
        self.excluido = True
        self.save()

class Equipamento(models.Model):
    categoria = models.CharField(
        max_length=10, choices=enums.EquipamentoCategoria.choices(), default='geral'
    )
    uf = models.CharField(max_length=2)
    proprietario = models.CharField(max_length=80)
    municipio = models.CharField(max_length=80)
    numero_serie = models.CharField(max_length=20)
    marca_modelo = models.CharField(max_length=80)
    cor = models.CharField(max_length=20)
    ano_fabricacao = models.CharField(max_length=4)
    combustivel = models.CharField(max_length=20)
    restricoes = models.TextField(null=True, blank=True)
    potencia = models.IntegerField(null=True, blank=True)
    horimetro = models.CharField(max_length=20, null=True, blank=True)
    excluido = models.BooleanField(default=False)
    data_cadastro = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=enums.EquipamentoStatus.choices())
    observacao = models.TextField(max_length=300, blank=True, null=True)

    def delete(self):
        self.excluido = True
        self.save()


class Funcionario(models.Model):
    nome = models.CharField(max_length=80)
    cargo = models.CharField(max_length=80)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField()
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=120)
    telefone = models.CharField(max_length=20)
    foto = models.ImageField(upload_to="funcionarios_fotos", null=True, blank=True)
    excluido = models.BooleanField(default=False)
    data_cadastro = models.DateField(auto_now_add=True)

    def delete(self):
        self.excluido = True
        self.save()

    def __str__(self):
        return self.nome


class Log(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class ItemServico(models.Model):
    descricao = models.CharField(max_length=255)


class Servico(models.Model):
    equipamento = models.ForeignKey(Equipamento, blank=True, null=True, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, blank=True, null=True, on_delete=models.CASCADE)
    data = models.DateField(blank=True, null=True)
    observacao = models.TextField(null=True, blank=True)
    itens = models.ManyToManyField(ItemServico, blank=True)
    data_saida = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)
    funcionario =  models.ForeignKey(Funcionario, blank=True, null=True, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    parecer = models.CharField(max_length=30, choices=enums.ServicoStatus.choices(), null=True, blank=True)
   
    def __str__(self):
        return f"Serviço para {self.equipamento or self.veiculo} em {self.data}"
    
    

class Contrato(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField(blank=True, null=True)
    data_termino = models.DateTimeField(blank=True, null=True)
    equipamento = models.ForeignKey(Equipamento, blank=True, null=True, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=enums.TipoStatus.choices(), blank=True, null=True)
    horas_funcionando = models.IntegerField(default=0)
    local_entrega = models.CharField(max_length=100, blank=True, null=True)
    data_evento = models.DateTimeField(blank=True, null=True)
    servicos_inclusos = models.TextField(blank=True, null=True)
    valor_aluguel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_equipamento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deposito_seguranca = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    taxas_adicionais = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    condicoes_especificas = models.TextField(blank=True, null=True)
    estado_inicial_gerador = models.TextField(blank=True, null=True)
    pago = models.BooleanField(default=False)
    tipo_pagamento = models.CharField(max_length=30, choices=enums.TipoPagamento.choices(), null=True, blank=True)
    data_pagamento = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.numero
