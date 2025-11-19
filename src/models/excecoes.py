class ErroRestauranteBase(Exception):
    #classe base para todas as exceções customizadas do sistema.
    def __init__(self, mensagem="Ocorreu um erro no sistema do restaurante."):
        self.mensagem = mensagem
        super().__init__(self.mensagem)

# erros de regra de negócio

class ErroDeRegraDeNegocio(ErroRestauranteBase):
    pass

class GarcomNoLimiteError(ErroDeRegraDeNegocio):
    pass

class GrupoNaoCabeNaMesaError(ErroDeRegraDeNegocio):
    pass

class EntidadeNaoEncontradaError(ErroDeRegraDeNegocio):
    pass

# erros de status/fluxo

class ErroDeStatusInvalido(ErroRestauranteBase):
    pass

class StatusMesaInvalidoError(ErroDeStatusInvalido):
    pass

class StatusPedidoInvalidoError(ErroDeStatusInvalido):
    pass

class ContaJaFechadaError(ErroDeStatusInvalido):
    pass

class ErroDePersistencia(ErroRestauranteBase):
    pass

class ArquivoCorrompidoError(ErroDePersistencia):
    pass