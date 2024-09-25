import logging
import re
from time import sleep
from typing import List, Dict, Any

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

from parsing_catalog_product.selection_of_categories import get_categories
from utils.delet_message import del_msg
from utils.state import StateProductSearch

# from parsing_catalog_product.options_for_parsing import PROXY

router: Router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(StateProductSearch.open_site)
async def get_store(message: Message, state: FSMContext) -> None:
    logger.info("launches a website magnit.ru")

    data = await state.get_data()
    user_agent = data["user_agent"]
    url = data["url"]
    service: Service = Service(executable_path=ChromeDriverManager().install())
    options: webdriver = webdriver.ChromeOptions()
    options.add_argument(f"User-Agent={user_agent}")
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    # options.add_argument(f"--proxy-server={PROXY}")
    options.add_argument(
        "--disable-extensions"
    )  # отключите расширения Chrome, чтобы обеспечить чистую среду автоматизации.
    options.add_argument(
        "--no-sandbox"
    )  # отключите режим sandbox, который может быть необходим в определенных средах.
    options.add_argument(
        "--disable-dev-shm-usage"
    )  # отключите использование общего пространства памяти dev-shm,
    # чтобы устранить потенциальные проблемы, связанные с памятью.
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )  # исключить коллекцию переключателей включения-автоматизации.
    options.add_experimental_option(
        "useAutomationExtension", False
    )  # отключить использование useAutomationExtension
    driver: webdriver = webdriver.Chrome(options=options, service=service)
    stealth(
        driver=driver,
        languages=["ru-RU", "ru", "en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=True,
    )  # надстройка предназначена для скрытия следов автоматизации
    driver.get(url=url)
    try:
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div/div[2]/button"
        ).click()  # кликаем на кнопку с cookie
        sleep(2)
    except NoSuchElementException:
        logger.exception("Missing button 'cookie'")
    driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/header/div[3]/div/div[2]/section/div[1]/div[1]/span",
    ).click()  # кликаем на кнопку с адресом
    sleep(2)
    await message.answer(text="Введите город")
    await state.update_data(driver=driver)
    await state.set_state(StateProductSearch.city_input)


@router.message(StateProductSearch.city_input)
async def get_city_input(message: Message, state: FSMContext) -> None:
    logger.info("The' user enters city")

    data: Dict[str, Any] = await state.get_data()
    driver: webdriver = data["driver"]
    field_input_city: webdriver = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/header/div[3]/div/div[2]/section/section/div"
        "/section[1]/div/div[3]/section/div/div[1]/form/div[1]/div/div/input",
    )
    field_input_city.clear()
    if re.fullmatch(r"[а-яё-]+", message.text.lower()):
        field_input_city.send_keys(message.text.lower())
        sleep(2)
        list_all_stores: List[webdriver] = driver.find_elements(
            By.CSS_SELECTOR,
            "section.shop-select__list-item--inner",
        )
        text: str = hbold("Список магазинов: \n")

        for num, store in enumerate(list_all_stores, start=1):
            text += f"{num}. {store.text.replace("Выбрать", "").rstrip()}\n"
        else:
            text += hbold("Введи номер для выбора магазина")

        await message.answer(text=text)
        await state.update_data(stores=list_all_stores)
        await state.set_state(StateProductSearch.store_selection)

    else:
        logger.warning("The user enters the city incorrectly")
        msg_city: Message = await message.answer(
            text=f"Название города должно быть на кириллице"
        )
        await del_msg(message)
        await del_msg(msg_city, 5)


@router.message(StateProductSearch.store_selection)
async def selecting_a_store_from_the_list(message: Message, state: FSMContext) -> None:
    logger.info("The user selects a city from the list")

    data: Dict[str, Any] = await state.get_data()
    list_all_stores = data["stores"]
    driver: webdriver = data["driver"]

    if message.text.isdigit() and 1 <= int(message.text) <= len(list_all_stores):
        await message.reply(
            text=f"{hbold('Выбрали магазин по адресу:')} \n"
            f"{list_all_stores[int(message.text) - 1].text.replace("Выбрать", "").rstrip()}"
        )
        list_all_stores[int(message.text) - 1].click()  # кликаем на магазин
        sleep(2)
        driver.find_element(
            By.XPATH, "//button[@class='pl-text shop-select__map__balloon__submit']"
        ).click()  # кликаем выбор магазина
        sleep(2)
        await state.set_state(StateProductSearch.categories)
        await get_categories(message, state)
    else:
        logger.warning("The user enters the city number incorrectly")
        msg_number: Message = await message.answer(
            text=f"Введите номер магазина из списка от 1 до {len(list_all_stores)}"
        )
        await del_msg(message)
        await del_msg(msg_number, 5)
