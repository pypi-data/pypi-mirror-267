from inewave.nwlistop.modelos.blocos.ree import REE
from inewave.nwlistop.modelos.arquivos.arquivoree import ArquivoREE
from inewave.nwlistop.modelos.vevmin import VevminAnos


class Vevmin(ArquivoREE):
    """
    Armazena os dados das saídas referentes às violações da meta
    de energia da vazão mínima, por REE.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `vevmin00x.out`, onde x varia conforme o
    REE em questão.

    """

    BLOCKS = [
        REE,
        VevminAnos,
    ]
