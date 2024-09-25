import csv
import logging
import os
from typing import Dict, Any

import aiofiles
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from bs4 import BeautifulSoup

from utils.state import StateProductSearch

router: Router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(StateProductSearch.parser)
async def parser_product(message: Message, state: FSMContext, catalog_dct=None) -> None:
    logger.info("Функция 'parser_product' парсит исходную страницу из файла")

    data: Dict[str, Any] = await state.get_data()
    url: str = data["url"]
    path_file_html: str = data["path_file_html"]
    name_category: str = data["name_category"]

    if catalog_dct is None:
        catalog_dct: Dict[int, Dict[str, str | float | int]] = {}

    async with aiofiles.open(path_file_html, "r", encoding="utf8") as file_out:
        src: str = await file_out.read()

    soup: BeautifulSoup = BeautifulSoup(src, "lxml")
    product_card = soup.find_all("a", class_="new-card-product")

    if product_card:
        for num, i_product in enumerate(product_card, start=1):
            catalog_dct.setdefault(num, {})

            product_title: str = i_product.find(
                "div", class_="new-card-product__title"
            ).text
            catalog_dct[num]["name"] = product_title

            product_price = i_product.find(
                "div", class_="new-card-product__price-regular"
            ).text
            catalog_dct[num]["price"] = float(
                product_price.replace(",", ".").replace("₽", "").rstrip()
            )

            price_old = i_product.find("div", class_="new-card-product__price-old")
            if price_old is not None:
                product_price_old: str = price_old.text
                catalog_dct[num]["price_old"] = float(
                    product_price_old.replace(",", ".").replace("₽", "").rstrip()
                )
                catalog_dct[num]["discount"] = round(
                    100
                    - (catalog_dct[num]["price"] / catalog_dct[num]["price_old"]) * 100
                )

            weight: Any = i_product.find("div", class_="new-card-product__weight")
            if weight is not None:
                product_weight: str = f"Индивидуальный вес: {weight.text}"
                catalog_dct[num]["weight"] = product_weight

            product_img: str = i_product.find("img").get("src")
            catalog_dct[num]["img"] = product_img

            product_url: str = f"{url[:-1]}{i_product.get('href')}"
            catalog_dct[num]["url"] = product_url

        path_file_csv = f"{name_category}.csv"
        async with aiofiles.open(
            path_file_csv, "w", newline="", encoding="windows-1251"
        ) as csv_file:
            fieldnames = [
                "name",
                "price",
                "price_old",
                "discount",
                "weight",
                "img",
                "url",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

            await writer.writeheader()
            for line in catalog_dct.values():
                await writer.writerow(line)

        await message.answer_document(document=FSInputFile(path=path_file_csv))
        os.remove(path_file_csv)
        logger.info("Поиск товара завершен, файл отправлен пользователю")

    else:
        await message.answer(text="Товар отсутствует в категории")
        logger.info("Поиск товара завершен, товар отсутствует в категории")

    await state.clear()
    os.remove(path_file_html)
