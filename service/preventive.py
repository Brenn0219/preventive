from time import sleep
from config import settings

def get_main_frame(page):
    page.wait_for_selector("iframe[name='gsft_main']", timeout=60000)
    return page.frame_locator("iframe[name='gsft_main']")


def fill_reference_field(frame, selector: str, value: str, delay_after_fill: float = 1.0):
    field = frame.locator(selector)

    field.wait_for(timeout=30000)
    field.click()
    field.fill(value)

    sleep(delay_after_fill)
    field.press("Tab")


def create_preventive(page, item: dict, logger):
    sector = item["setor"]            
    request_type = item["tipo"]        
    location = item["local"]           
    assignee = item["atribuido"]       
    
    logger.info(f"Creating preventive: {sector} ({request_type})")

    frame = get_main_frame(page)

    new_button = frame.locator("#sysverb_new")
    new_button.wait_for(timeout=30000)
    new_button.click()

    frame.locator(
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assignment_group"
    ).wait_for(timeout=30000)

    fill_reference_field(
        frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assignment_group",
        settings.GROUP,
        delay_after_fill=1.0
    )

    fill_reference_field(
        frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.assigned_to",
        assignee,
        delay_after_fill=1.0
    )

    fill_reference_field(
        frame,
        "#sys_display\\.u_tarefas_rotineiras_de_fieldservice\\.location",
        location,
        delay_after_fill=2.0  
    )

    select_tipo = frame.locator(
        "#u_tarefas_rotineiras_de_fieldservice\\.u_tipo_de_solicita_o"
    )
    select_tipo.wait_for(timeout=30000)

    tipo_option = settings.TYPE_MAP[request_type]

    select_tipo.select_option(tipo_option)

    frame.locator(
        "#u_tarefas_rotineiras_de_fieldservice\\.u_nome_do_setor"
    ).fill(str(sector))

    frame.locator(
        "#u_tarefas_rotineiras_de_fieldservice\\.description"
    ).fill(settings.DESCRIPTION[request_type])

    frame.locator("#sysverb_insert_bottom").click()
    page.wait_for_load_state("networkidle")