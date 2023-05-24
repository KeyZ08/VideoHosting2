import json
import os

from django.db.models import Count, Q
from django.http import JsonResponse

from users.CastomException import DisplayedException
from users.models import Video, User, Comments

host = os.getenv('HOST', "http://127.0.0.1:8000")


def get_video(id_video, published=False):
    try:
        video = Video.objects.get(id_video=id_video)
        if published and not video.published:
            return JsonResponse(status=400, data={"error": "Видео не найдено."})
        info = _get_all_public_info_about_video(video)
        return JsonResponse(status=200, data={"status": "ok", "data": info})
    except Exception as e:
        print(e)
        return JsonResponse(status=400, data={"error": "Видео не найдено."})


def get_p_videos(username):
    return _get_videos_by_user(username, True)


def get_h_videos(username):
    return _get_videos_by_user(username, False)


def _get_videos_by_user(username: str, published: bool = False) -> JsonResponse:
    try:
        videos = User.objects.get(username=username).video_set.filter(published=published).order_by('-date')
        data = []
        for i in videos:
            data.append(_get_public_info_about_video(i))
        return JsonResponse(status=200, data={"status": "ok", "data": data})
    except Exception as e:
        print(e)
        return JsonResponse(status=404, data={"status": "error", "error": "Пользователь не найден"})


def get_comments(id_video):
    try:
        comments = Comments.objects.filter(video=id_video)
        data = []
        for i in comments:
            c = {
                "author": _get_public_info_about_user(i.username),
                "comment": {
                    "id_video": i.video.id_video,
                    "text": i.text,
                    "date": i.date,
                    "comment_id": i.id,
                }
            }
            data.append(c)
        return JsonResponse(status=200, data={"status": "ok", "data": data})
    except:
        return JsonResponse(status=400, data={"status": "error", "error": "Что-то пошло не так."})


def get_video_history(username):
    try:
        user = User.objects.get(username=username)
        history = user.history_set.values().order_by("-date")
        data = []
        for i in history:
            video = JsonUnpacker(get_video(id_video=i["video_id"]))
            video["video"]["viewing_date"] = i["date"]
            data.append(video)
        return JsonResponse(status=200, data={"status": "ok", "data": data})
    except:
        return JsonResponse(status=400, data={"status": "error", "error": "Пользователь не найден"})


def get_most_popular_videos(count: int):
    try:
        videos = Video.objects.filter(published=True).annotate(views_count=Count("history")).order_by("-views_count")
        data = []
        for video in videos:
            if count == 0:
                break
            data.append(_get_all_public_info_about_video(video))
            count -= 1
        return JsonResponse(status=200, data={"status": "ok", "data": data})
    except Exception as e:
        print(e)
        return JsonResponse(status=404, data={"status": "error", "error": "Не удалось выполнить запрос"})


def get_new_videos(count: int):
    try:
        videos = Video.objects.filter(published=True).order_by("-date")
        data = []
        for video in videos:
            if count == 0:
                break
            data.append(_get_all_public_info_about_video(video))
            count -= 1
        return JsonResponse(status=200, data={"status": "ok", "data": data})
    except Exception as e:
        print(e)
        return JsonResponse(status=404, data={"status": "error", "error": "Не удалось выполнить запрос"})


def get_all_videos():
    try:
        videos = Video.objects.filter(published=True).order_by("-date")
        data = []
        for i in videos:
            data.append(_get_all_public_info_about_video(i))
        return JsonResponse(status=200, data={"status": "ok", "data": data})
    except:
        return JsonResponse(status=400, data={"status": "error", "error": "Что-то пошло не так."})


def get_all_users():
    try:
        users = User.objects.annotate(video_count=Count("video", filter=Q(video__published=True)))
        data = []
        for i in users:
            user = _get_public_info_about_user(i)
            user["video_count"] = i.video_count
            data.append(user)
        return JsonResponse(status=200, data={"status": "ok", "data": data})
    except:
        return JsonResponse(status=400, data={"status": "error", "error": "Что-то пошло не так."})


def _get_all_public_info_about_video(video):
    obj = {
        "video": _get_public_info_about_video(video),
        "author": _get_public_info_about_user(video.username)
    }
    return obj


def _get_public_info_about_video(video):
    obj = {
        "id_video": video.id_video.__str__(),
        "title": video.title,
        "description": video.description,
        "preview": video.get_absolute_preview_url(),
        "video": video.get_absolute_video_url(),
        "url": host + "/videos/" + video.id_video.__str__(),
        "user": video.username.username,
        "date": video.date,
        "views_count": video.history_set.count(),
        "likes_count": video.likes_set.count(),
        "dislikes_count": video.dislikes_set.count(),
        "comments_count": video.comments_set.count(),
    }
    return obj


def _get_public_info_about_user(user):
    obj = {
        "name": user.name,
        "username": user.username,
        "url": host + "/accounts/" + user.username.__str__(),
        "avatar": user.get_absolute_url_avatar(),
    }
    return obj


def JsonUnpacker(json_response: JsonResponse):
    data = json.loads(json_response.content)
    if data["status"] != "ok":
        raise DisplayedException(data["error"])
    return data["data"]


def jsonrpc_error(error_message: str, code: int):
    return {"error": {"message": error_message, "code": code}, "id": "0", "jsonrpc": "2.0"}


def jsonrpc_result(result: dict):
    return {"result": result, "id": "0", "jsonrpc": "2.0"}
