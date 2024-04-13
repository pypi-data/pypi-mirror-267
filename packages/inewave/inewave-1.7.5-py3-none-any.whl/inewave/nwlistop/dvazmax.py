from inewave.nwlistop.modelos.blocos.usina import Usina
from inewave.nwlistop.modelos.arquivos.arquivousinapatamar import (
    ArquivoUsinaPatamar,
)
from inewave.nwlistop.modelos.dvazmax import DvazmaxAnos


class Dvazmax(ArquivoUsinaPatamar):
    """
    Armazena os dados das saídas referentes à violação de restrição de
    vazão máxima por usina.

    Esta classe lida com as informações de saída fornecidas pelo
    NWLISTOP e reproduzidas nos `dvazmax00x.out`, onde x varia conforme
    a usina em questão.

    """

    BLOCKS = [
        Usina,
        DvazmaxAnos,
    ]
