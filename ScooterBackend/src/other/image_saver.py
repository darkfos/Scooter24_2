from fastapi import UploadFile
from os import remove
from typing import Union
import shutil

class ImageSaver:
    def __init__(self) -> None:
        self.init_url: str = "src/static/"
        self.filename: str = ""

    async def generate_filename(self, id_: int, filename: str) -> None:
        self.filename = filename + "__" + str(id_) 

    async def save_file(self, file: UploadFile) -> Union[None, str]:
        try:
            with open(file=self.init_url+self.filename, mode="wb") as file_catalog:
                shutil.copyfileobj(file.file, file_catalog)
            return self.filename
        except Exception as ex:
            return False

    async def remove_file(self) -> bool:
        try:
            remove(path=self.init_url+self.filename)
            return True
        except Exception as ex:
            return False