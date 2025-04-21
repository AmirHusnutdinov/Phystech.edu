import boto3
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError
from typing import List, Dict, Optional
from settings import app

class Cloud:
    def __init__(self):
        try:
            self.BUCKET_MAIN_PATH = app.config.get("BUCKET_MAIN_PATH")
            self.ENDPOINT_URL = app.config.get("ENDPOINT_URL")
            self.REGION_NAME = app.config.get("REGION_NAME")
            self.ACC_ACCESS_KEY = app.config.get("ACC_ACCESS_KEY")
            self.ACC_SECRET_KEY = app.config.get("ACC_SECRET_KEY")

            if not all([self.BUCKET_MAIN_PATH, self.ENDPOINT_URL, self.ACC_ACCESS_KEY, self.ACC_SECRET_KEY]):
                raise ValueError("Не все обязательные параметры конфигурации заданы")

            self.s3_client = boto3.client(
                "s3",
                endpoint_url=self.ENDPOINT_URL,
                region_name=self.REGION_NAME,
                aws_access_key_id=self.ACC_ACCESS_KEY,
                aws_secret_access_key=self.ACC_SECRET_KEY,
            )

            self._test_connection()

        except NoCredentialsError:
            raise Exception("Не удалось найти учетные данные AWS")
        except EndpointConnectionError:
            raise Exception(f"Не удалось подключиться к endpoint: {self.ENDPOINT_URL}")
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == 'InvalidAccessKeyId':
                raise Exception("Неверный ключ доступа AWS")
            elif error_code == 'SignatureDoesNotMatch':
                raise Exception("Неверная секретная подпись AWS")
            else:
                raise Exception(f"Ошибка клиента S3: {str(e)}")
        except Exception as e:
            raise Exception(f"Ошибка инициализации Cloud: {str(e)}")

    def _test_connection(self):
        """Проверка соединения с хранилищем"""
        try:
            self.s3_client.head_bucket(Bucket=self.BUCKET_MAIN_PATH)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404':
                raise Exception(f"Бакет {self.BUCKET_MAIN_PATH} не найден")
            elif error_code == '403':
                raise Exception(f"Нет доступа к бакету {self.BUCKET_MAIN_PATH}")
            else:
                raise

    def get_url(self, file_key: str) -> Optional[str]:
        """
        Возвращает presigned URL для одного файла
        
        Args:
            file_key: Путь к файлу в хранилище
            
        Returns:
            URL файла или None, если файл не существует
        """
        try:
            self.s3_client.head_object(Bucket=self.BUCKET_MAIN_PATH, Key=file_key)
            return self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.BUCKET_MAIN_PATH, 'Key': file_key},
                ExpiresIn=3600
            )
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None
            raise Exception(f"Ошибка доступа к файлу {file_key}: {str(e)}")

    def get_urls_batch(self, file_keys: List[str]) -> Dict[str, Optional[str]]:
        """
        Возвращает словарь presigned URL для списка файлов
        
        Args:
            file_keys: Список путей к файлам в хранилище
            
        Returns:
            Словарь вида {'file_key': 'url'} (None для отсутствующих файлов)
        """
        result = {}
        for file_key in file_keys:
            try:
                url = self.get_url(file_key)
                result[file_key] = url
            except Exception as e:
                result[file_key] = None
        return result
    
    def get_folder(self, folder_path: str) -> Dict[str, Optional[str]]:
        """
        Возвращает словарь presigned URL для всех файлов в указанной папке
        
        Args:
            folder_path: Путь к папке в хранилище (например, 'images/')
            
        Returns:
            Словарь вида {'file_key': 'url'} для всех файлов в папке
        """
        if not folder_path.endswith('/'):
            folder_path += '/'
        
        try:
            # Получаем список объектов в папке
            response = self.s3_client.list_objects_v2(
                Bucket=self.BUCKET_MAIN_PATH,
                Prefix=folder_path,
                Delimiter='/'
            )
            
            if 'Contents' not in response:
                return {}
            
            # Фильтруем только файлы (исключаем подпапки)
            file_keys = [item['Key'] for item in response['Contents'] 
                    if not item['Key'].endswith('/')]
            
            # Генерируем URL для каждого файла
            return self.get_urls_batch(file_keys)
            
        except ClientError as e:
            raise Exception(f"Ошибка при получении списка файлов из папки {folder_path}: {str(e)}")

    def add_picture(self, file_path: str, file_key: str) -> str:
        """
        Загружает файл в хранилище и возвращает его URL
        
        Args:
            file_path: Локальный путь к файлу
            file_key: Путь назначения в хранилище
            
        Returns:
            URL загруженного файла
        """
        try:
            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=self.BUCKET_MAIN_PATH,
                Key=file_key
            )
            return self.get_url(file_key)
        except FileNotFoundError:
            raise Exception(f"Локальный файл не найден: {file_path}")
        except ClientError as e:
            raise Exception(f"Ошибка загрузки в S3: {str(e)}")
        except Exception as e:
            raise Exception(f"Ошибка при добавлении файла: {str(e)}")

    def file_exists(self, file_key: str) -> bool:
        """Проверяет существование файла в хранилище"""
        try:
            self.s3_client.head_object(Bucket=self.BUCKET_MAIN_PATH, Key=file_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise