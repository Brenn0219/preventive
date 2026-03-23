from config import settings

def get_main_frame(page):
    page.wait_for_selector("iframe[name='gsft_main']")
    return page.frame(name="gsft_main")


def fill_reference_field(frame, selector: str, value: str):
    field = frame.locator(selector)

    field.click()
    field.fill(value)

    # ServiceNow precisa de TAB para validar campo
    frame.wait_for_timeout(1500)
    field.press("Tab")


def create_preventive(page, item: dict, logger):
    sector = item["setor"]
    request_type = item["tipo"]

    logger.info(f"Creating preventive: {sector} ({request_type})")

    frame = get_main_frame(page)

    # Aguarda botão "Novo"
    frame.wait_for_selector("#sysverb_new", timeout=settings.TIMEOUT)
    frame.click("#sysverb_new")

    # Preenche campos
    fill_reference_field(
        frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assignment_group",
        settings.GROUP
    )

    fill_reference_field(
        frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assigned_to",
        settings.ASSIGNEE
    )

    fill_reference_field(
        frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.location",
        settings.LOCATION
    )

    # Tipo (select)
    frame.select_option(
        "#u_tarefas_rotineiras_de_fieldservice\\.u_tipo_de_solicita_o",
        settings.TYPE_MAP[request_type]
    )

    # Nome do setor
    frame.fill(
        "#u_tarefas_rotineiras_de_fieldservice\\.u_nome_do_setor",
        sector
    )

    # Descrição
    frame.fill(
        "#u_tarefas_rotineiras_de_fieldservice\\.description",
        settings.DESCRIPTION[request_type]
    )

    # Enviar
    frame.click("#sysverb_insert_bottom")

    frame.wait_for_timeout(3000)