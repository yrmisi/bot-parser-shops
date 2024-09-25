import logging
from time import sleep
from typing import Dict, Any, List

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from selenium import webdriver
from selenium.webdriver.common.by import By

from parsing_catalog_product.product_search import get_product
from utils.delet_message import del_msg
from utils.state import StateProductSearch

router: Router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(StateProductSearch.categories)
async def get_categories(message: Message, state: FSMContext) -> None:
    logger.info("Функция 'get_categories' выводит каталог товаров")

    data: Dict[str, Any] = await state.get_data()
    driver: webdriver = data["driver"]

    button_all_products = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/main/div/div/section[2]/div/ul/li[8]/a",
    )
    sleep(2)
    driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/header/div[3]/div/div[1]/div[1]/div[1]/div[1]/button",
    ).click()  # кликаем выбор категории
    sleep(2)
    select_category: List[webdriver] = driver.find_elements(
        By.CSS_SELECTOR,
        "div.pl-list-item.pl-list-item_primary.header-catalog-item",
    )
    select_category.insert(0, button_all_products)

    text: str = hbold("Все категории магазина\n")
    for num, category in enumerate(select_category, start=1):
        if num == 1:
            text += f"{num}. {category.get_attribute("title")}\n"
        else:
            text += f"{num}. {category.text}\n"
    text += hbold("Выберите номер категории")

    await message.answer(text=text)
    await state.update_data(categories=select_category)
    await state.set_state(StateProductSearch.category_number)


@router.message(StateProductSearch.category_number)
async def get_enter_category_number(message: Message, state: FSMContext) -> None:
    logger.info(
        "Функция 'get_enter_category_number' пользователь вводит номер категории"
    )
    data: Dict[str, Any] = await state.get_data()
    driver: webdriver = data["driver"]
    select_category: List[webdriver] = data["categories"]
    text: str = hbold("Выбрали категорию \n")

    if message.text.isdigit() and 1 <= int(message.text) <= len(select_category):
        button_category = select_category[int(message.text) - 1].click()
        sleep(300)
        if isinstance(button_category, str):
            text += "Все товары"
            name_category = "Все товары"
        else:
            text += button_category.text
            name_category = button_category.text
        await message.reply(text=text)
        await state.update_data(name_category=name_category)

        if isinstance(button_category, str):
            driver.get(url=button_category)

        else:
            button_category.click()
            all_products_of_the_selected_category: webdriver = driver.find_element(
                By.XPATH, "/html/body/main/header/div[4]/div[2]/div/ul[2]/li[3]/a"
            ).get_attribute("href")
            driver.get(url=all_products_of_the_selected_category)

        await state.update_data(driver=driver)
        await state.set_state(StateProductSearch.product)
        await get_product(message, state)

    else:
        logger.error(
            "Функция 'get_enter_category_number' некорректно вводит номер категории"
        )
        msg: Message = await message.answer(
            text=f"Введите номер категории из списка от 1 до {len(select_category)}"
        )
        await del_msg(message)
        await del_msg(msg, 5)
