import json

from users.CastomException import DisplayedException
from datetime import datetime, timezone, timedelta


def get_signature(file, type):
    """
    Смотрит на первые байты файла для более точного определения его расширения (сигнатуры)

    :param file: первые 256 байт файла
    :param type: ожидаемый тип файла (image / video)
    :return: сигнатуру (png, mp4 и тд) или строку 'Неизвестная сигнатура'
    """
    image_signature = {
        "FF D8 FF E0": "jpg",
        "49 46 00 01": "jpeg",
        "89 50 4E 47 0D 0A 1A 0A": "png",
    }

    video_signature = {
        "1A 45 DF A3": "webm",
        "66 74 79 70 4D 53 4E 56": "mp4",
        "66 74 79 70 69 73 6F 6D": "mp4",
    }
    if type == "video":
        signature = video_signature
    elif type == "image":
        signature = image_signature
    else:
        raise Exception("Нереализованный тип")
    hex_bytes = " ".join(['{:02X}'.format(byte) for byte in file])
    for hex_ch in signature:
        for i in [0, 12]:
            if hex_ch == str(hex_bytes[i:len(hex_ch) + i]):
                return signature.get(hex_ch)
    return "Неизвестная сигнатура"


def video_change_check(title, description):
    """
    Задает ограничения для title и description

    :return: DisplayedException если что-то некорректно
    """
    if title.__len__() < 5:
        raise DisplayedException("Минимум 5 символов.")
    if title.__len__() > 100:
        raise DisplayedException("Максимум 100 символов.")
    if description.__len__() > 3000:
        raise DisplayedException("Максимум 3000 символов.")


def time_since_upload(str_datetime):
    """
    Вычисляет как давно видео было загружено

    :param str_datetime: строка формата iso (пример: 2023-04-22T15:25:03.062Z)
    :return:
    """
    upload_time = datetime.fromisoformat(str_datetime.replace("Z", "+00:00"))
    time_since = datetime.now(timezone.utc) - upload_time
    if time_since < timedelta(minutes=1):
        return 'только что'
    elif time_since < timedelta(hours=1):
        return f'{time_since.seconds // 60} минут назад'
    elif time_since < timedelta(days=1):
        return f'{time_since.seconds // 3600} часов назад'
    elif time_since < timedelta(days=30):
        return f'{time_since.days} дней назад'
    elif time_since < timedelta(days=365):
        return f'{time_since.days // 30} месяцев назад'
    else:
        return f'{time_since.days // 365} лет назад'


def check_file_valid(file_name, file_size, file_target):
    """

    :param file_name: имя файла с расширением (например: text.png)
    :param file_size: размер файла
    :param file_target: назначение файла
    :return: DisplayedException если файл не удовлетворяет условиям
    """
    check_file({"name": file_name, "target": file_target, "size": file_size})


def check_file(file):
    target = file["target"]
    if target == "avatar_image":
        supported_types = ["jpg", "png", "jpeg"]
        max_size = 1024 * 512  # 0,5MB
    elif target == "video_preview_image":
        supported_types = ["jpg", "png", "jpeg"]
        max_size = 1024 * 1024  # 1MB
    elif target == "video":
        supported_types = ["mp4", "webm"]
        max_size = 1024 * 1024 * 1024  # 1GB
    else:
        raise DisplayedException("Неизвестный target.")
    if not (file["name"].split('.')[-1] in supported_types):
        raise DisplayedException(f"Неподдерживаемый тип данных. Поддерживаются: {' '.join(supported_types)}")
    if file["size"] > max_size:
        raise DisplayedException(f"Слишком большой файл. Максимум {max_size / 1024.0 / 1024}MB")