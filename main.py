import time

from config import settings
from service.logger import get_logger
from service.playwright import start_browser
from service.excel_reader import load_excel
from service.preventive import create_preventive

logger = get_logger()

def execute_with_retry(func, *args):
    for attempt in range(1, settings.MAX_RETRY + 1):
        try:
            func(*args)
            return True

        except Exception as e:
            logger.error(f"Error on attempt {attempt}: {e}")

            if attempt == settings.MAX_RETRY:
                logger.error("Final failure")
                return False

            logger.info("Retrying...")
            time.sleep(3)

def main():
    logger.info("Starting automation")

    data = load_excel(settings.EXCEL_PATH)

    playwright, browser, page = start_browser()

    page.goto(settings.URL)

    logger.info("Manual login required...")
    page.wait_for_timeout(30000)

    for item in data:
        execute_with_retry(create_preventive, page, item, logger)

    logger.info("Automation finished")

    browser.close()
    playwright.stop()


if __name__ == "__main__":
    main()