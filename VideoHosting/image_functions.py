import uuid
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import UploadedFile

from VideoHosting.additional_functions import get_signature, check_file_valid
from users.vk_open import delete_object, load


def _img_crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    # Функция для обрезки изображения по центру.
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def _img_crop_max_square(pil_img) -> Image:
    return _img_crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def _img_crop_max_rectangle(pil_img) -> Image:
    k = 16.0 / 9.0
    w, h = pil_img.size
    new_w, new_h = w, h
    if min(pil_img.size) == h:
        new_w = k * h
        if new_w > w:
            new_w = w
            new_h = w / k
    else:
        new_h = w / k
        if new_h > h:
            new_h = h
            new_w = k * h
    return _img_crop_center(pil_img, new_w, new_h)


def load_userImage(file: UploadedFile, user):
    buffer, path = _load_img(file, "avatar_image")
    try:
        load(buffer, path)
        user.avatar = path
        user.save()
    except:
        delete_object(path)


def load_videoImage(file: UploadedFile, video):
    buffer, path = _load_img(file, "video_preview_image")
    try:
        load(buffer, path)
        video.preview = path
        video.save()
    except:
        delete_object(path)


def _load_img(file, target):
    if target != "video_preview_image" and target != "avatar_image":
        raise Exception("Неизвестный target")
    buffer = BytesIO()
    buf = file.read(256)
    sig = get_signature(buf, 'image')
    if sig == "jpg": sig = "jpeg"
    check_file_valid(f"x.{sig}", file.size, target)
    buffer.write(buf)
    buffer.write(file.read())

    img = Image.open(buffer)
    path = ""
    if target == "video_preview_image":
        path = f"videos/images/{uuid.uuid4()}.{file.name.split('.')[-1]}"
        img = _img_crop_max_rectangle(img)
    elif target == "avatar_image":
        path = f"users/avatars/{uuid.uuid4()}.{file.name.split('.')[-1]}"
        img = _img_crop_max_square(img)
    buffer = BytesIO()
    img.save(buffer, format=sig)
    buffer.seek(0)
    return buffer, path

