from contextlib import asynccontextmanager

from aiobotocore.session import ClientCreatorContext, AioSession, get_session

# Local
from src.settings.engine_settings import Settings


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
            "region_name": "ru-1"
        }


        self.session: AioSession = get_session()

    @asynccontextmanager
    async def get_client_session(self) -> ClientCreatorContext:
        """
        Получаем сессию для работы с S3
        """

        async with self.session.create_client("s3", **self.__s3_config) as cl_session:
            yield cl_session

    async def upload_file_to_storage(self, file, is_saved: bool = False) -> bool:
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
                        res = await cl_session.put_object(
                            Bucket=self.__bucket_name,
                            Key="products/"+file_name,
                            Body=fl,
                        )
                else:
                    file_name = file.filename
                    await cl_session.put_object(
                        Bucket=self.__bucket_name,
                        Key=f"products/{file_name}",
                        Body=await file.read()
                    )

                return f"https://5e3cd16e-1044-41ad-a814-7534a2520dd6.selstorage.ru/products%2F{file_name}"
        except Exception as ex:
            print(ex)
            return False
        else:
            return True
