from script.config import settings
from script.service.logger import get_logger
from script.service.playwright import start_browser
from script.service.preventive import create_preventive
from db.db import Database
from script.repository.sectors import SectorsReadRepository

logger = get_logger()

def main():
    logger.info("Iniciando Automacao")

    db = Database()
    db.initialize()

    sectors_repo = SectorsReadRepository(db)

    data = sectors_repo.get_all()

    playwright, browser, page = start_browser()

    page.goto(settings.URL)

    logger.info("Login Manual...")
    page.wait_for_timeout(30000)

    for item in data:
        try:
            create_preventive(page, item, logger)
        except Exception as e:
            logger.error(f"Erro ao criar preventiva para {item['setor']}: {e}")
            continue

    logger.info("Automacao Finalizada")

    browser.close()
    playwright.stop()


if __name__ == "__main__":
    main()