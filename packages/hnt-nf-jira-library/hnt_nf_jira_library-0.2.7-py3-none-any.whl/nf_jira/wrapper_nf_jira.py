import json
import requests
import os
from os import getcwd, path
from datetime import datetime
from pydantic import ValidationError

from .entities.nota_pedido import NotaPedido
from .entities.miro import Miro
from .entities.constants import *
from .entities.classes.form_jira import FormJira
from .entities.classes.issue_jira import IssueJira
from .entities.classes.issue_jira import AttachmentJira
from .entities.classes.issue_fields import IssueFields
from .entities.classes.helper import JiraFieldsHelper, JsonHelper

from nf_consumo.consumo_service import ConsumoService


class wrapper_jira:

    def __init__(self, debug=False):
        self._test_mode = debug
        self._set_request()
        self.FormJira         = FormJira()
        self.IssueJira        = IssueJira()
        self.AttachmentJira   = AttachmentJira()
        self.JiraFieldsHelper = JiraFieldsHelper()
        self.JsonHelper       = JsonHelper()
        self.IssueFields      = IssueFields()
        self.ConsumoService   = ConsumoService()

    def _set_request(self):
        self._api_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _issue_factory(self, issue: dict):

        sintese_itens = []
        validTotalPercents = 0.0

        if not issue["allocation_data"]:

            item = {
                "centro": issue["domain_data"]["centro"]["centro"],
                "centro_custo": f"{issue['domain_data']['centro']['centro']}210",
                "cod_imposto": "C6",
                "valor_bruto": str(issue["json_data"][VALOR_TOTAL_DA_FATURA]),
            }

            sintese_item = {
                "categoria_cc": "K",
                "quantidade": 1,
                "cod_material": issue["domain_data"]["fornecedor"]["codigo_material"],
                "item": item,
            }

            sintese_itens.append(sintese_item)

        else:

            for centro_issue in issue["allocation_data"]["centro_custos"]:

                validTotalPercents += float(centro_issue["porcentagem"])

                item = {
                    "centro": centro_issue["nome"].split("210")[0],
                    "centro_custo": centro_issue["nome"],
                    "cod_imposto": "C6",
                    "valor_bruto": "{:.2f}".format(
                        issue["json_data"][VALOR_TOTAL_DA_FATURA]
                        * float(centro_issue["porcentagem"])
                        / 100,
                        2,
                    ),
                }

                sintese_item = {
                    "categoria_cc": "K",
                    "quantidade": 1,
                    "cod_material": issue["domain_data"]["fornecedor"][
                        "codigo_material"
                    ],
                    "item": item,
                }

                sintese_itens.append(sintese_item)

            if validTotalPercents != 100.0:
                raise Exception(f"Invalid total percentage: {validTotalPercents}%")

        anexo = {
            "path": issue["pdf_data"]["path_dir"],
            "filename": issue["pdf_data"]["filename"],
        }

        nota_pedido = {
            "tipo": "ZCOR",
            "org_compras": issue["domain_data"]["centro"]["org_compras"],
            "grp_compradores": issue['json_data']['grupo_compradores'][0],
            "empresa": "HFNT",
            "cod_fornecedor": issue["domain_data"]["fornecedor"]["codigo_sap"],
            "sintese_itens": sintese_itens,
            "anexo": anexo,
            "jira_info": issue["jira_info"],
        }

        return nota_pedido

    def _miro_factory(self, issue: dict):

        data_ref = issue[DATA_DE_REFERÊNCIA](
            datetime.strptime(issue[DATA_DE_REFERÊNCIA], "%m/%Y")
            .strftime("%b/%y")
            .upper()
        )

        if issue[COMPLEMENTO_DE_ÁGUA] is not None:
            leitura_anterior = (
                datetime.strptime(
                    issue[COMPLEMENTO_DE_ÁGUA]["DataLeituraAnterior"],
                    "%Y-%m-%dT%H:%M:%S",
                )
                .strftime("%b/%y")
                .upper()
            )
            leitura_atual = (
                datetime.strptime(
                    issue[COMPLEMENTO_DE_ÁGUA]["DataLeituraAtual"], "%Y-%m-%dT%H:%M:%S"
                )
                .strftime("%b/%y")
                .upper()
            )
        elif issue[COMPLEMENTO_DE_ENERGIA] is not None:
            leitura_anterior = (
                datetime.strptime(
                    issue[COMPLEMENTO_DE_ENERGIA]["DataLeituraAnterior"],
                    "%Y-%m-%dT%H:%M:%S",
                )
                .strftime("%b/%y")
                .upper()
            )
            leitura_atual = (
                datetime.strptime(
                    issue[COMPLEMENTO_DE_ENERGIA]["DataLeituraAtual"],
                    "%Y-%m-%dT%H:%M:%S",
                )
                .strftime("%b/%y")
                .upper()
            )
        elif issue[COMPLEMENTO_DE_GÁS] is not None:
            leitura_anterior = (
                datetime.strptime(
                    issue[COMPLEMENTO_DE_GÁS]["DataLeituraAnterior"],
                    "%Y-%m-%dT%H:%M:%S",
                )
                .strftime("%b/%y")
                .upper()
            )
            leitura_atual = (
                datetime.strptime(
                    issue[COMPLEMENTO_DE_GÁS]["DataLeituraAtual"], "%Y-%m-%dT%H:%M:%S"
                )
                .strftime("%b/%y")
                .upper()
            )

        texto = f"REF: {data_ref} PERIODO: {leitura_anterior} A {leitura_atual}"

        dados_basicos = {
            "data_da_fatura": datetime.strptime(
                issue[DATA_DE_EMISSÃO], "%Y-%m-%dT%H:%M:%S"
            ).strftime("%d%m%Y"),
            "referencia": f"{issue['ChaveAcessoNotaFiscal'][25:34]}-{issue['ChaveAcessoNotaFiscal'][22:25]}",
            "montante": str(issue[VALOR_TOTAL_DA_FATURA]),
            "texto": texto,
        }

        referencia_pedido = {"numero_pedido": issue["cod_sap"]}

        detalhe = {"ctg_nf": issue["domain_data"]["fornecedor"]["categoria_nf"]}

        sintese = {"CFOP": issue["domain_data"]["fornecedor"]["cfop"]}

        chave_acesso = {
            "numero_aleatorio": f"{issue['ChaveAcessoNotaFiscal'][35:43]}",
            "dig_verif": f"{issue['ChaveAcessoNotaFiscal'][43:]}",
        }

        nfe_sefaz = {
            "numero_log": issue["numero_log"],
            "data_procmto": issue["data_procmto"],
            "hora_procmto": issue["hora_procmto"],
        }

        dados_nfe = {"chave_acesso_sefaz": chave_acesso, "nfe_sefaz": nfe_sefaz}

        miro_model = {
            "dados_basicos": dados_basicos,
            "referencia_pedido": referencia_pedido,
            "detalhe": detalhe,
            "sintese": sintese,
            "dados_nfe": dados_nfe,
        }

        return miro_model

    def get_nf_issue_context(self, issue_id: str):
        try:

            issue_json = self._get_nf_jira(issue_id)

            attachment = issue_json["attachment"]
            jira_info = issue_json["jira_info"]

            ##### GET DOMAIN #####
            ## FORNECEDOR
            cnpj_fornecedor = attachment.get(CNPJ_DO_FORNECEDOR)
            fornecedor = self._get_nf_domain("fornecedor", cnpj_fornecedor)

            ## CENTRO
            cnpj_centro = attachment.get(CNPJ_DO_CLIENTE)
            centro = self._get_nf_domain("centro", cnpj_centro)

            domain = {"fornecedor": fornecedor, "centro": centro}

            ##### GET PDF #####
            pdf_data = self._download_pdf(attachment[ARQUIVOS_DA_FATURA][0])

            ##### GET ALLOCATION #####
            allocation = self._get_allocation(
                attachment[CNPJ_DO_FORNECEDOR],
                attachment[CNPJ_DO_CLIENTE],
                attachment[NÚMERO_DO_CONTRATO],
            )

            ##### FORMAT JSON #####
            issue = {
                "issue_data": issue_json["issue_data"],
                "json_data": attachment,
                "domain_data": domain,
                "allocation_data": allocation,
                "pdf_data": pdf_data,
                "jira_info": jira_info,
            }

            ##### PARSE JSON #####
            issue_model = self._issue_factory(issue)

            ##### CREATE MODEL #####
            nota_pedido = NotaPedido(**issue_model).model_dump()

            #### SAVE JSON ####
            if self._test_mode:
                self.JsonHelper.save_json(f'Nota_Pedido_{issue_id}', nota_pedido)

            return nota_pedido
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

        except Exception as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

    def get_nf_miro_context(self, issue_id: str, cod_sap: str):
        try:

            issue_data = self._get_nf_jira(issue_id)

            clean_fields = self._remove_null_fields(
                issue_data["issue_data"].get("fields")
            )
            issue_data["issue_data"]["fields"] = clean_fields

            attachment = issue_data["attachment"]
            attachment["cod_sap"] = cod_sap

            ##### GET DOMAIN #####
            ## FORNECEDOR
            cnpj_fornecedor = attachment.get(CNPJ_DO_FORNECEDOR)
            fornecedor = self._get_nf_domain("fornecedor", cnpj_fornecedor)

            ## CENTRO
            cnpj_centro = attachment.get(CNPJ_DO_CLIENTE)
            centro = self._get_nf_domain("centro", cnpj_centro)

            attachment["domain_data"] = {"fornecedor": fornecedor, "centro": centro}

            miro_model = self._miro_factory(attachment)

            miro = Miro(**miro_model).model_dump()

            if self._test_mode:
                self.JsonHelper.save_json(f'Miro_{issue_id}', miro)

            return miro

        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

        except Exception as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

    def _get_nf_jira(self, issue_id: str):
        try:

            issue_data = self.IssueJira.get_issue(issue_id)
            complement_form = self._get_issue_fields_by_keys( issue_id, FORM_TEMPLATE_COMPLEMENTO )

            issue_data["fields"] = self.JiraFieldsHelper.remove_null_fields(issue_data.get("fields"))
            attachment = self.AttachmentJira.get_attachment(issue_data)

            nf_type_id = complement_form["tipo_conta"]

            if nf_type_id == "ÁGUA":
                nf_type = COMPLEMENTO_DE_ÁGUA

            elif nf_type_id == "ENERGIA":
                nf_type = COMPLEMENTO_DE_ENERGIA

            elif nf_type_id == "GÁS":
                nf_type = COMPLEMENTO_DE_GÁS

            else:
                if attachment[COMPLEMENTO_DE_ÁGUA] is not None:
                    nf_type = COMPLEMENTO_DE_ÁGUA
                elif attachment[COMPLEMENTO_DE_ENERGIA] is not None:
                    nf_type = COMPLEMENTO_DE_ENERGIA
                elif attachment[COMPLEMENTO_DE_GÁS] is not None:
                    nf_type = COMPLEMENTO_DE_GÁS

            attachment[CNPJ_DO_FORNECEDOR] = complement_form['cnpj_fornecedor']
            attachment[RAZÃO_SOCIAL_DO_FORNECEDOR] = complement_form['razao_social_fornecedor']

            attachment[CNPJ_DO_CLIENTE] = complement_form['cnpj_destinatario']
            attachment[NÚMERO_DA_FATURA] = complement_form['nro_nota_fiscal']
            attachment[NÚMERO_DA_FATURA_DO_FORNECEDOR] = complement_form['nro_fatura']
            attachment[DATA_DE_EMISSÃO] = complement_form['data_emissao']
            attachment[DATA_DE_VENCIMENTO] = complement_form['data_vencimento']
            attachment[CHAVE_DE_ACESSO_DA_FATURA] = complement_form['chave_acesso']
            attachment[DATA_DE_REFERÊNCIA] = complement_form['periodo_referencia']
            attachment["numero_log"] = complement_form['protocolo_autorizacao']
            attachment["data_procmto"] = complement_form['data_autorizacao']
            attachment["hora_procmto"] = complement_form['hora_autorizacao']
            attachment[nf_type]["DataLeituraAnterior"] = complement_form['data_leitura_anterior']
            attachment[nf_type]["DataLeituraAtual"] = complement_form['data_leitura_atual']
            attachment["grupo_compradores"] = complement_form['grupo_compradores']
            attachment["grupo_compradores"] = complement_form['grupo_compradores']

            #Validação de Valor Liquido da Fatura
            if complement_form['valor_liquido'] != None:
                attachment[VALOR_TOTAL_DA_FATURA] = complement_form['valor_liquido']
            elif complement_form['valor_nota'] != None:
                attachment[VALOR_TOTAL_DA_FATURA] = complement_form['valor_nota']
            else:
                attachment[VALOR_TOTAL_DA_FATURA] = attachment.get(
                    VALOR_TOTAL_DA_FATURA
                )

            automation_form_id = self.FormJira.get_form_id(issue_id, FORM_TEMPLATE_AUTOMACAO)

            jira_info = {"issue_id": issue_id, "form_id": automation_form_id}

            nf_jira_json = {
                "issue_data": issue_data,
                "attachment": attachment,
                "jira_info": jira_info,
            }

            return nf_jira_json

        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

        except Exception as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

    def _get_nf_domain(self, type: str, cnpj: str):

        try:
            domain_request = requests.get(
                f"{API_DOMAIN_N8N_URL}/{'fornecedores' if type == 'fornecedor' else 'centros'}?cnpj={cnpj}",
                auth=N8N_AUTH,
            )
            domain_request.raise_for_status()
            domain_data = domain_request.json()

            if not domain_data:
                raise Exception("Could not find domain")

        except Exception as e:
            raise Exception(f"Erro ao receber {type}:\n{e}")

        return domain_data

    def _get_allocation(
        self, cnpj_fornecedor: str, cnpj_cliente: str, numero_contrato: str
    ):

        try:
            allocation_request = requests.get(
                f"{API_DOMAIN_N8N_URL}/rateio?cnpj_fornecedor={cnpj_fornecedor}&cnpj_hortifruti={cnpj_cliente}&numero_contrato={numero_contrato}",
                auth=N8N_AUTH,
            )
            allocation_request.raise_for_status()
            if allocation_request.text.strip() != "":
                allocation_data = allocation_request.json()
            else:
                allocation_data = None
        except Exception as e:
            raise Exception(f"Erro ao receber rateio:\n{e}")

        return allocation_data

    def _download_pdf(self, pdf_path):
        path_dir = path.join(getcwd(), "output/pdf")
        pdf_file = self.ConsumoService.download_pdf(pdf_path, path_dir)

        return pdf_file



    def post_transition(self, transition_id, issue_id):
        payload = json.dumps(
            {
                "transition": {"id": transition_id},
                "update": {"comment": []},
            }
        )
        res = requests.post(
            f"{self._api_issue_url}/issue/{issue_id}/transitions",
            auth=JIRA_AUTH,
            headers=API_HEADERS,
            data=payload,
        )
        res.raise_for_status()

    def _get_issue_fields_by_keys(self, issue_key, form_template):

        form_jira_keys = self.FormJira.get_form_jira_keys(issue_key, form_template)
        form_fields    = self.FormJira.get_form_fields(issue_key, form_template)
        jira_fields    = self.IssueJira.get_issue_fields_data(issue_key)
        fields_by_jira_and_form = self.IssueFields.get_fields_by_form_and_jira(form_jira_keys, form_fields, jira_fields)

        return fields_by_jira_and_form
