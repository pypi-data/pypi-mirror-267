import logging
from hnt_sap_gui.common.sap_status_bar import sbar_extracted_text

logger = logging.getLogger(__name__)
MSG_SAP_CODIGO_DOCUMENTO = "^Documento ([0-9]*) HFNT foi pré-editado$"
class FaturaTransaction:
    def __init__(self) -> None:
        pass

    def execute(self, sapGuiLib, fatura):
        logger.info(f"Enter execute fatura:{fatura}")
        sapGuiLib.run_transaction('/nFV60')
        # ABA DADOS BÁSICOS
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpMAIN/ssubPAGE:SAPLFDCB:0010/ctxtINVFO-ACCNT").Text = fatura['dados_basicos']['cod_fornecedor']
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpMAIN/ssubPAGE:SAPLFDCB:0010/ctxtINVFO-BLDAT").Text = fatura['dados_basicos']['data_fatura']
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpMAIN/ssubPAGE:SAPLFDCB:0010/txtINVFO-XBLNR").Text = fatura['dados_basicos']['referencia']
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpMAIN/ssubPAGE:SAPLFDCB:0010/txtINVFO-WRBTR").Text = fatura['dados_basicos']['montante']
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpMAIN/ssubPAGE:SAPLFDCB:0010/ctxtINVFO-BUPLA").Text = fatura['dados_basicos']['bus_pl_sec_cd']
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpMAIN/ssubPAGE:SAPLFDCB:0010/ctxtINVFO-SGTXT").Text = fatura['dados_basicos']['texto']
        sapGuiLib.send_vkey(0)

        for i, iten in enumerate(fatura['dados_basicos']['itens']):
            sapGuiLib.session.findById("wnd[0]/usr/subITEMS:SAPLFSKB:0100/tblSAPLFSKBTABLE/ctxtACGL_ITEM-HKONT[1,0]").Text = iten['Cta_razao']
            sapGuiLib.session.findById("wnd[0]/usr/subITEMS:SAPLFSKB:0100/tblSAPLFSKBTABLE/txtACGL_ITEM-WRBTR[4,0]").Text = iten['Montante']
            sapGuiLib.session.findById("wnd[0]/usr/subITEMS:SAPLFSKB:0100/tblSAPLFSKBTABLE/ctxtACGL_ITEM-BUPLA[6,0]").Text = iten['loc_negocios']
            sapGuiLib.session.findById("wnd[0]/usr/subITEMS:SAPLFSKB:0100/tblSAPLFSKBTABLE/txtACGL_ITEM-ZUONR[10,0]").Text = iten['atribuicao']
            sapGuiLib.session.findById("wnd[0]/usr/subITEMS:SAPLFSKB:0100/tblSAPLFSKBTABLE/ctxtACGL_ITEM-SGTXT[12,0]").Text = iten['texto']
            sapGuiLib.session.findById("wnd[0]/usr/subITEMS:SAPLFSKB:0100/tblSAPLFSKBTABLE/ctxtACGL_ITEM-KOSTL[18,0]").Text = iten['centro_custo']
            
            sapGuiLib.session.findById("wnd[0]/usr/subITEMS:SAPLFSKB:0100/tblSAPLFSKBTABLE").verticalScrollbar.Position = i

        sapGuiLib.send_vkey(0)
        # ABA DADOS PAGAMENTO
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpPAYM").Select()
        sapGuiLib.send_vkey(0)
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpPAYM/ssubPAGE:SAPLFDCB:0020/cmbINVFO-ZLSPR").Key = ""
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpPAYM/ssubPAGE:SAPLFDCB:0020/ctxtINVFO-ZFBDT").Text = fatura['pagamento']['data_basica']
        sapGuiLib.session.findById("wnd[0]/usr/tabsTS/tabpPAYM/ssubPAGE:SAPLFDCB:0020/ctxtINVFO-ZTERM").Text = fatura['pagamento']['cond_pgto']
        sapGuiLib.send_vkey(0)
        sapGuiLib.send_vkey(0)

        sapGuiLib.session.findById("wnd[0]/tbar[0]/btn[11]").press()
        documento = sbar_extracted_text(MSG_SAP_CODIGO_DOCUMENTO,
                                              sapGuiLib.session.findById("wnd[0]/sbar").Text)
        return documento

