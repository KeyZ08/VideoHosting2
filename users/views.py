import uuid
from io import BytesIO

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST

from VideoHosting.additional_functions import time_since_upload, video_change_check, check_file_valid, get_signature
from VideoHosting.image_functions import load_userImage, load_videoImage

from django.contrib.auth import authenticate, login
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt

from users.forms import UserCreationForm, UserChangeForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app_api.internal_api import *
from .models import Video, User, Likes, Dislikes, Comments
from .vk_open import delete_object, load


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

        context = {'form': form}
        return render(request, self.template_name, context)


def account(request, username=None):
    if username is not None:
        try:
            user = User.objects.get(username=username)
            p_videos = json.loads(get_p_videos(user.username).content)
            if p_videos["status"] != "ok":
                raise Exception("Ошибка")
            else:
                p_videos = p_videos["data"]

            for i in p_videos:
                i["date"] = time_since_upload(i["date"])

            data = {
                "avatar": user.get_absolute_url_avatar(),
                "username": user.username,
                "name": user.name,
                "date_joined": user.date_joined,
                "birthday": user.birthday,
                "p_videos": p_videos,
            }
            return render(request, "users/account_public.html", data)
        except ObjectDoesNotExist as e:
            return render(request, "users/Error.html", {"message": "Пользователь не найден"})
        except Exception as e:
            print("Exeption in account:", e)
            return e

    if not request.user.is_authenticated:
        return redirect("login")

    user = User.objects.get(username=request.user.username)

    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            data = {
                "avatar": user.get_absolute_url_avatar(),
                "username": user.username,
                "date_joined": user.date_joined,
                "form": form,
            }
            return render(request, "users/account.html", data)

    else:
        form = UserChangeForm(instance=user)
        p_videos = json.loads(get_p_videos(user.username).content)
        h_videos = json.loads(get_h_videos(user.username).content)
        if p_videos["status"] != "ok":
            raise Exception("Ошибка")
        else:
            p_videos = p_videos["data"]

        for i in p_videos:
            i["date"] = time_since_upload(i["date"])

        if h_videos["status"] != "ok":
            raise Exception("Ошибка")
        else:
            h_videos = h_videos["data"]
        data = {
            "avatar": user.get_absolute_url_avatar(),
            "username": user.username,
            "date_joined": user.date_joined,
            "form": form,
            "p_videos": p_videos,
            "h_videos": h_videos
        }
        return render(request, "users/account.html", data)


@csrf_exempt
def video_change(request, id_video):
    try:
        video = Video.objects.get(id_video=id_video)
        if video.username != request.user:
            return JsonResponse(status=403, data=jsonrpc_error("Несоответствие владельца видео.", 403))
    except:
        return render(request, "users/Error.html", {"message": "Видео не найдено."})

    if request.method == 'POST':
        if int(request.headers.get("content_length")) > 1024 * 1024 + 1024 * 50:  # 1MB + 50КБ
            return JsonResponse(status=413, data=jsonrpc_error("Слишком большой запрос", 413))
        try:
            title = request.POST["title"].strip()
            descr = request.POST["description"].strip()
            published = request.POST["published"] == "true"
            video_change_check(title, descr)
            video.title = title
            video.description = descr
            video.published = published
            video.save()
            if request.FILES.get("preview", None) is not None:
                img: UploadedFile = request.FILES["preview"]
                load_videoImage(img, video)
            return JsonResponse(status=200, data=jsonrpc_result({"status": "ok"}))
        except DisplayedException as e:
            return JsonResponse(status=400, data=jsonrpc_error(e.__str__(), 400))
        except Exception as e:
            return JsonResponse(status=520, data=jsonrpc_error("Неизвестная ошибка", 520))
    else:
        try:
            video = Video.objects.get(id_video=id_video)
        except:
            return render(request, "users/Error.html", {"message": "Видео не найдено."})

        data = {"video_url": video.get_absolute_video_url(),
                "preview": video.get_absolute_preview_url(),
                "title": video.title,
                "description": video.description,
                "published": video.published,
                "id_video": video.id_video}
        return render(request, "users/video_change.html", context=data)


@csrf_exempt
def avatar_upload(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=405,
                            data=jsonrpc_error("Для выполнения этого действия вам нужно авторизоваться", 405))
    if request.method == "POST":
        if int(request.headers.get("content_length")) > 1024 * 1024 * 0.5 + 1024 * 50:  # 0.5MB + 50КБ
            return JsonResponse(status=413, data=jsonrpc_error("Слишком большой запрос", 413))

        try:
            buffer, signature = write_and_check_userImage(request)
            buffer.seek(0)

            file = UploadedFile(file=buffer, size=buffer.__sizeof__(), name=f"x.{signature}")
            load_userImage(file, request.user)
            return JsonResponse(status=200,
                                data=jsonrpc_result({"status": 'ok', "url": request.user.get_absolute_url_avatar()}))
        except DisplayedException as e:
            return JsonResponse(status=415, data=jsonrpc_error(e.__str__(), 415))
        except Exception as e:
            print("\nError:", e, "\n")
            return JsonResponse(status=520, data=jsonrpc_error("Неизвестная ошибка", 520))
    else:
        return JsonResponse(status=403, data=jsonrpc_error("Доступ только через POST", 403))


@csrf_exempt
def avatar_reset(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=405,
                            data=jsonrpc_error("Для выполнения этого действия вам нужно авторизоваться", 405))
    if request.method == "POST":
        try:
            request.user.avatar = "users/avatars/default_avatar.jpg"
            request.user.save()
        except:
            return JsonResponse(status=520, data=jsonrpc_error("Неизвестная ошибка", 520))
        return JsonResponse(status=200,
                            data=jsonrpc_result({"status": 'ok', "url": request.user.get_absolute_url_avatar()}))
    else:
        return JsonResponse(status=403, data=jsonrpc_error("Доступ только через POST", 403))


@csrf_exempt
def video_upload(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=405,
                            data=jsonrpc_error("Для выполнения этого действия вам нужно авторизоваться", 405))

    if request.method == "POST":
        path = "unknown"
        try:
            buffer, signature = write_and_check_video(request)
            buffer.seek(0)
            nvideo = Video(username=request.user)
            path = f"videos/{nvideo.id_video}.{signature}"
            load(file=buffer, path=path)
            nvideo.file = path
            nvideo.save()
            return JsonResponse(status=200, data=jsonrpc_result({"next_url": f'/videos/{nvideo.id_video}/change/'}))
        except DisplayedException as e:
            if path != "unknown":
                delete_object(path)
            return JsonResponse(status=415, data=jsonrpc_error(e.__str__(), 415))
        except Exception as e:
            print(e)
            if path != "unknown":
                delete_object(path)
            return JsonResponse(status=520, data=jsonrpc_error("Неизвестная ошибка", 520))
    else:
        return JsonResponse(status=403, data=jsonrpc_error("Доступ только через POST", 403))


@csrf_exempt
def video_delete(request, id_video):
    if not request.user.is_authenticated:
        return JsonResponse(status=405,
                            data=jsonrpc_error("Для выполнения этого действия вам нужно авторизоваться", 405))
    if request.method == "POST":
        try:
            video = Video.objects.get(username=request.user, id_video=id_video)
            video.delete()
            return JsonResponse(status=200, data=jsonrpc_result({"status": 'ok', "next_url": "/account/"}))
        except:
            return JsonResponse(status=403,
                                data=jsonrpc_error("Несоответствие владельца, либо видео несуществует", 403))
    else:
        return JsonResponse(status=403, data=jsonrpc_error("Доступ только через POST", 403))


@csrf_exempt
def like(request, id_video):
    if not request.user.is_authenticated:
        return JsonResponse(status=405,
                            data=jsonrpc_error("Для выполнения этого действия вам нужно авторизоваться", 405))
    if request.method == "POST":
        if not id_video:
            return JsonResponse(status=400, data=jsonrpc_error("Не указано id_video", 400))
        try:
            video = Video.objects.get(id_video=id_video)
            like, like_created = Likes.objects.get_or_create(video=video, username=request.user)
            if like_created:
                like.save()
            else:
                like.delete()
            return JsonResponse(status=200,
                                data=jsonrpc_result({"status": "ok",
                                                     "liked": like_created, "disliked": False,
                                                     "likes_count": video.likes_set.count(),
                                                     "dislikes_count": video.dislikes_set.count()}))
        except Exception as e:
            print(e)
            return render(request, "users/Error.html", {"message": "Видео не найдено."})
    else:
        return JsonResponse(status=403, data=jsonrpc_error("Доступ только через POST", 403))


@csrf_exempt
def dislike(request, id_video):
    if not request.user.is_authenticated:
        return JsonResponse(status=405,
                            data=jsonrpc_error("Для выполнения этого действия вам нужно авторизоваться", 405))
    if request.method == "POST":
        if not id_video:
            return JsonResponse(status=400, data=jsonrpc_error("Не указано id_video", 400))
        try:
            video = Video.objects.get(id_video=id_video)
            dislike, dislike_created = Dislikes.objects.get_or_create(video=video, username=request.user)
            if dislike_created:
                dislike.save()
            else:
                dislike.delete()
            return JsonResponse(status=200,
                                data=jsonrpc_result({"status": "ok",
                                                     "liked": False, "disliked": dislike_created,
                                                     "likes_count": video.likes_set.count(),
                                                     "dislikes_count": video.dislikes_set.count()}))
        except Exception as e:
            print(e)
            return render(request, "users/Error.html", {"message": "Видео не найдено."})
    else:
        return JsonResponse(status=403, data=jsonrpc_error("Доступ только через POST", 403))


def add_comment(request, id_video):
    video = get_object_or_404(Video, id_video=id_video)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.user
            comment.video = video
            comment.save()
        return redirect('video', id_video=id_video)
    else:
        form = CommentForm()

    context = {
        'video': video,
        'form': form,
    }
    return render(request, 'basic_pages/video.html', context)


@csrf_exempt
def delete_comment(request, comment_id, id_video):
    comment = get_object_or_404(Comments, id=comment_id)
    if request.method == 'POST' and request.user == comment.username:
        comment.delete()
        return JsonResponse({'deleted': True})
    return JsonResponse({'deleted': False})


def video_history(request):
    if not request.user.is_authenticated:
        return redirect("login")
    try:
        history = JsonUnpacker(get_video_history(request.user.username))
        for i in history:
            i["video"]["date"] = time_since_upload(i["video"]["date"])
            i["video"]["viewing_date"] = time_since_upload(i["video"]["viewing_date"])
        return render(request, "basic_pages/history_videos.html", context={"videos": history})
    except Exception as e:
        print(e)
        return render(request, "users/Error.html", {"message": "Произошла непредвиденная ошибка."})


def write_and_check_video(request):
    return write_and_check_file(request, "video", "video", 1024 * 1024 * 1024)  # 1GB


def write_and_check_userImage(request):
    return write_and_check_file(request, "image", "avatar_image", 1024 * 1024 * 0.5)  # 0.5MB


def write_and_check_file(request, file_type, target, max_size):
    chunk_size = 1024 * 1024 * 2  # 2MB
    content_size = int(request.headers.get("content_length"))
    file_size = 0
    buffer = BytesIO()
    data = request.read(256)
    s = get_signature(data, file_type)
    check_file_valid(f"x.{s}", content_size, target)
    buffer.write(data)
    file_size += len(data)
    while True:
        data = request.read(chunk_size)
        if not data:
            break
        buffer.write(data)
        file_size += len(data)
        if file_size > content_size or file_size > max_size:
            raise DisplayedException("Несоответствие размера передаваемого файла")
    if file_size != content_size:
        raise DisplayedException("Несоответствие размера передаваемого файла")
    return buffer, s

# метод генерации авторизованной ссылки для загрузки файлов
# def create_presigned_post(request: WSGIRequest):
#     data = json.loads((request.body.decode('utf-8')))
#     print(data)
#     if not data['name']:
#         return HttpResponse(status=400, content="invalid request body")
#
#     session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
#     s3_client: BaseClient = session.client(service_name=SERVICE_NAME, endpoint_url=ENDPOINT_URL)
#     try:
#         response = s3_client.generate_presigned_url(ClientMethod='put_object',
#                                                     Params={'Bucket': AWS_STORAGE_BUCKET_NAME,
#                                                             'Key': data["name"]},
#                                                     ExpiresIn=3600,
#                                                     HttpMethod='PUT')
#     except ClientError as e:
#         logging.error(e)
#         return HttpResponse(status=500, content=json.load(e.response))
#     print(response)
#     return JsonResponse({'url': response})
