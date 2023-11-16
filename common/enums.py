from enum import Enum, unique


class BaseEnum(str, Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)


@unique
class ClienteTipo(BaseEnum):
    FISICA: str = "fisica"
    JURIDICA: str = "juridica"


@unique
class EquipamentoStatus(BaseEnum):
    DISPONIVEL: str = "disponivel"
    INDISPONIVEL: str = "indisponivel"


@unique
class EquipamentoCategoria(BaseEnum):
    GERADOR: str = "gerador"
    VEICULO: str = "veiculo"
    ILUMINACAO: str = "iluminacao"
    GERAL: str = "geral"

@unique
class ServicoStatus(BaseEnum):
    APROVADO: str = "aprovado"
    APROVADO_COM_RESSALVA: str = "aprovado_com_ressalva"
    PENDENTE: str = "pendente"
    REPROVADO: str = "reprovado"