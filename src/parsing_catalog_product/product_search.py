import datetime
import logging
from time import sleep
from typing import Dict, Any

import aiofiles
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from selenium import webdriver
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By

from parsing_catalog_product.parsing_of_goods import parser_product
from utils.state import StateProductSearch

router: Router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(StateProductSearch.product)
async def get_product(message: Message, state: FSMContext, page=None) -> None:
    logger.info(
        "Функция 'get_product' загружает в файл исходную html разметку категории"
    )

    data: Dict[str, Any] = await state.get_data()
    driver = data["driver"]
    current_date: datetime = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    sleep(3)
    try:
        button_age_18: webdriver = driver.find_element(
            By.XPATH, "//button[@class='alcohol__button alcohol__success ']"
        )
        button_age_18.click()
    except ElementNotInteractableException:
        logger.error("Отсутствует кнопка 'button_age_18' возрастные ограничения")

    if page is None:
        pressing_the_button: bool = True
    else:
        pressing_the_button: int = page
        pressing_the_button -= 1

    while pressing_the_button:
        if type(pressing_the_button) is int:
            pressing_the_button -= 1
        try:
            button_show_more: webdriver = driver.find_element(
                By.XPATH, "//div[@class='paginate__more']"
            )
            button_show_more.click()
            sleep(2)
        except ElementNotInteractableException:
            logger.error("Отсутствует кнопка 'button_show_more' показать еще")
            pressing_the_button: bool = False

    path_file_html: str = f"{current_date}_catalog.html"

    async with aiofiles.open(path_file_html, "w", encoding="utf8") as file:
        await file.write(driver.page_source)

    driver.close()
    driver.quit()

    await state.update_data(path_file_html=path_file_html)
    await state.set_state(StateProductSearch.parser)
    await parser_product(message, state)


if __name__ == "__main__":
    ...
