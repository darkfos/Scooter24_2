from fastapi import UploadFile
from os import remove
from typing import Union, Type
from src.api.authentication.hash_service.hashing import CryptographyScooter
import shutil
import logging


class ImageSaver:
    def __init__(self) -> None:
        self.init_url: str = "src/static/images/"
        self.filename: str = ""

    async def generate_filename(self, id_: int, filename: str) -> None:
        self.filename: str = str(id_) + "__" + filename

    # aiofiles - async
    async def save_file(
        self, file: Type[UploadFile], is_admin: bool = False
    ) -> Union[None, str]:
        try:
            if is_admin:
                crypt: Type[CryptographyScooter] = CryptographyScooter()
                await self.generate_filename(
                    id_=crypt.hashed_img(img_name=file.filename)[0::5],
                    filename=file.filename,
                )

                # Logging
                logging.info(
                    msg="Image Saver (Admin Panel)"
                    " сохранение фотографии в директории"
                )

                with open(
                    file=self.init_url + self.filename, mode="wb"
                ) as file_catalog:
                    shutil.copyfileobj(file.file, file_catalog)
            else:
                # Logging
                logging.info(msg="Image Saver сохранение" "фотографии в директории")
                with open(
                    file=self.init_url + self.filename, mode="wb"
                ) as file_catalog:
                    shutil.copyfileobj(file.file, file_catalog)
            return self.filename
        except Exception:
            logging.exception(msg="Image Saver Не удалось сохранить файл")
            return False

    async def remove_file(self) -> bool:
        try:
            # Logging
            logging.info(msg="Image Saver Картинка была успешно удалена")
            remove(path=self.init_url + self.filename)
            return True
        except Exception:
            # Logging
            logging.exception(msg="Image Saver не удалось удалить картинку")
            return False
