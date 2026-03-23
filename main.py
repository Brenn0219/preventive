from playwright.sync_api import sync_playwright, TimeoutError
import pandas as pd
import logging
import time

URL = "https://yduqs.service-now.com/now/nav/ui/classic/params/target/u_tarefas_rotineiras_de_fieldservice_list.do%3Fsysparm_nostack%3Dtrue%26sysparm_userpref_module%3Dd66ca38b3b015a10ce7e936765e45a1b"

GRUPO = "SN_TI_FIELD_SERVICE_N1"
RESPONSAVEL = "Pedro Henrique Fernandes Costa"
LOCAL = "INSTITUTO CULTURAL NEWTON PAIVA - CARLOS LUZ"

DESCRICAO = {
    "sala": "Preventiva de sala de aula: verificação de equipamentos, rede e funcionamento geral.",
    "lab": "Preventiva de laboratório de informática: verificação de máquinas, rede, periféricos e funcionamento geral."
}

TIPO_MAP = {
    "sala": "5",
    "lab": "2"
}

MAX_RETRY = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("automacao.log"),
        logging.StreamHandler()
    ]
)


def preencher_referencia(frame, selector, valor):
    campo = frame.locator(selector)

    campo.click()
    campo.fill(valor)
    frame.wait_for_timeout(1500)

    campo.press("Tab")

def get_frame(page):
    page.wait_for_selector("iframe[name='gsft_main']")
    return page.frame(name="gsft_main")

def criar_preventiva(page, setor, tipo):
    tipo = tipo.lower().strip()

    logging.info(f"Criando preventiva: {setor} ({tipo})")

    frame = get_frame(page)

    frame.wait_for_selector("#sysverb_new", timeout=60000)
    frame.click("#sysverb_new")

    frame.wait_for_selector("#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assignment_group")

    preencher_referencia(frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assignment_group",
        GRUPO
    )

    preencher_referencia(frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assigned_to",
        RESPONSAVEL
    )

    preencher_referencia(frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.location",
        LOCAL
    )

    frame.select_option(
        "#u_tarefas_rotineiras_de_fieldservice\\.u_tipo_de_solicita_o",
        TIPO_MAP[tipo]
    )

    frame.fill(
        "#u_tarefas_rotineiras_de_fieldservice\\.u_nome_do_setor",
        setor
    )

    frame.fill(
        "#u_tarefas_rotineiras_de_fieldservice\\.description",
        DESCRICAO[tipo]
    )

    frame.click("#sysverb_insert_bottom")


def executar_com_retry(func, *args):
    for tentativa in range(1, MAX_RETRY + 1):
        try:
            func(*args)
            return True
        except Exception as e:
            logging.error(f"Erro na tentativa {tentativa}: {e}")

            if tentativa == MAX_RETRY:
                logging.error("Falha definitiva ❌")
                return False

            logging.info("Tentando novamente...")
            time.sleep(3)


def carregar_excel(caminho):
    df = pd.read_excel(caminho)

    if "SETOR" not in df.columns or "TIPO" not in df.columns:
        raise Exception("Excel deve ter colunas: setor, tipo")

    return df.to_dict(orient="records")


# ================= MAIN =================

def run():
    dados = carregar_excel("setores-np-cl.xlsx")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(URL)

        logging.info("Faça login manual...")
        page.wait_for_timeout(30000)

        for item in dados:
            executar_com_retry(
                criar_preventiva,
                page,
                str(item["SETOR"]),
                item["TIPO"]
            )

        logging.info("Finalizado!")

        browser.close()


if __name__ == "__main__":
    run()