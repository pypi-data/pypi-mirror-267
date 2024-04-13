import logging
from SapGuiLibrary import SapGuiLibrary
from dotenv import load_dotenv

from hnt_sap_gui.nota_fiscal.fatura_transaction import FaturaTransaction

from .common.session import sessionable
from .nota_fiscal.nota_pedido_transaction import NotaPedidoTransaction
from .nota_fiscal.liberacao_transaction import LiberacaoTransaction

logger = logging.getLogger(__name__)

class SapGui(SapGuiLibrary):
    def __init__(self) -> None:
        load_dotenv()
        pass

    @sessionable
    def hnt_run_transaction(self, data):
        logger.info(f"enter execute run_hnt_transactions data:{data}")
        codigo = NotaPedidoTransaction().execute(self, nota_pedido=data)
        cod_liberacao = LiberacaoTransaction().execute(self, codigo)
        result = {
            "codigo": codigo,
            "cod_liberacao": cod_liberacao
        }
        logger.info(f"leave execute run_hnt_transactions result{str(result)}")
        return result
        
    @sessionable
    def hnt_run_transaction_FV60(self, data):
        cod_documento = FaturaTransaction().execute(self, data)
        logger.info(f"leave execute hnt_run_transaction_FV60 cod_documento: '{cod_documento}'")
        return cod_documento
