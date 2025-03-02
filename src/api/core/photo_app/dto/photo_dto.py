from pydantic import BaseModel, Field
from typing import Annotated, List


class PhotoBase(BaseModel):
    photo_url: Annotated[str, Field()]


class AllPhotos(BaseModel):
    photos: Annotated[List[PhotoBase], Field()]
