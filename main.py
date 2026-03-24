from config import settings
from service.logger import get_logger
from service.playwright import start_browser
from service.excel_reader import load_excel
from service.preventive import create_preventive

logger = get_logger()

def main():
    logger.info("Starting automation")

    data = load_excel(settings.EXCEL_PATH)

    playwright, browser, page = start_browser()

    page.goto(settings.URL)

    logger.info("Manual login required...")
    page.wait_for_timeout(30000)

    for item in data:
        try:
            create_preventive(page, item, logger)
        except Exception as e:
            logger.error(f"Erro ao criar preventiva para {item['setor']}: {e}")
            continue

    logger.info("Automation finished")

    browser.close()
    playwright.stop()


if __name__ == "__main__":
    main()