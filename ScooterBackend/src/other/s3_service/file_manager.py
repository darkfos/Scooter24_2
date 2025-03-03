import io
from contextlib import asynccontextmanager
from aiohttp import ClientSession
from aiobotocore.session import ClientCreatorContext, AioSession, get_session

# Local
from settings.engine_settings import Settings
from other.enums.s3_storage_enums import S3EnumStorage


class FileS3Manager:
    def __init__(
        self,
    ):
        self.__access_key: str = Settings.cloud_settings.S3_ACCESS_KEY
        self.__secret_key: str = Settings.cloud_settings.S3_SECRET_KEY
        self.__endpoint_url: str = Settings.cloud_settings.SELECTEL_URL
        self.__bucket_name: str = Settings.cloud_settings.CLOUD_NAME

        # Конфигурация
        self.__s3_config = {
            "aws_access_key_id": self.__access_key,
            "aws_secret_access_key": self.__secret_key,
            "endpoint_url": self.__endpoint_url,
            "region_name": "ru-1",
        }

        self.session: AioSession = get_session()

    @asynccontextmanager
    async def get_client_session(self) -> ClientCreatorContext:
        """
        Получаем сессию для работы с S3
        """

        async with self.session.create_client(
            "s3", **self.__s3_config
        ) as cl_session:
            yield cl_session

    async def upload_file_to_storage(
        self, file, directory: S3EnumStorage, is_saved: bool = False
    ) -> bool:
        """
        Загрузка файла в хранилище
        :param file:
        :return:
        """

        try:
            async with self.get_client_session() as cl_session:
                if is_saved:
                    file_name = file.split("/")[-1]
                    with open(file, "rb") as fl:
                        await cl_session.put_object(
                            Bucket=self.__bucket_name,
                            Key=directory + "/" + file_name,
                            Body=fl,
                        )
                else:
                    file_name = file.filename
                    await cl_session.put_object(
                        Bucket=self.__bucket_name,
                        Key=f"{directory}/{file_name}",
                        Body=await file.read(),
                    )

                return (
                    Settings.cloud_settings.S3_STORAGE_URL
                    + f"/{directory}%2F"  # noqa
                    + file_name  # noqa
                )  # noqa
        except Exception:
            return False
        else:
            return True

    async def upload_file_from_url(
        self, url_file: str, file_name: str, directory: S3EnumStorage
    ) -> str:
        """
        Загрузка файла из сторонней ссылки
        :param url_file:
        :param file_name:
        :return:
        """

        try:
            async with self.get_client_session() as cl_session:
                # Получаем файл
                async with ClientSession() as req:
                    async with req.get(url_file) as ai_req:
                        file = io.BytesIO(await ai_req.read())
                        file.seek(0)

                    await cl_session.put_object(
                        Bucket=self.__bucket_name,
                        Key=f"{directory}/{file_name}",
                        Body=file.read(),
                    )

                return (
                    Settings.cloud_settings.S3_STORAGE_URL
                    + f"/{directory}%2F"  # noqa
                    + file_name  # noqa
                )  # noqa
        except Exception as ex:
            print(ex, "#" * 15)
            return None
