"""
У вас есть некая система, выдающая и принимающая обратно свой бэкап в виде потока байтов.
Бэкап может занимать до 10 TiB.

Есть ресурсоемкий алгоритм сжатия/шифрования позволяющий (относительно медленно) сжимать/шифровать поток данных.
Данные сжимаются примерно в 1.5-3 раза.

И есть сетевое хранилище (тоже относительно медленное), которое позволяет сохранять файлы.
Размер одного файла в хранилище не может превышать 100 MiB.
Предполагается, что внутри Folder содержится 1 бэкап и изначально Folder пустой.
"""
from abc import ABC, abstractmethod
import io


class Processor(ABC):
    @abstractmethod
    def compress_and_encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt_and_uncompress(self, data: bytes) -> bytes:
        pass


class Folder(ABC):
    @abstractmethod
    async def write_file(self, name: str, data: bytes):
        pass

    @abstractmethod
    async def read_file(self, name: str) -> bytes:
        pass

    @abstractmethod
    async def list_files(self) -> list[str]:
        pass


"""
Необходимо реализовать функции `save_backup` и `restore_backup`,
реализующие сохранение бэкапа из потока в сетевое хранилище и восстановление обратно:
"""

async def save_backup(processor: Processor, folder: Folder, stream: io.BufferedReader):
    counter = 1
    while data := stream.read(104857600):
        data = processor.compress_and_encrypt(data)
        await folder.write_file(str(counter), data)
        counter += 1

async def restore_backup(processor: Processor, folder: Folder, stream: io.BufferedWriter):
    l = await folder.list_files()
    l.sort(key=int)
    for data in l:
        file = await folder.read_file(data)
        stream.write(processor.decrypt_and_uncompress(file))

