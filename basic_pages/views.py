from django.shortcuts import render
from datetime import datetime
from django.utils import timezone as djtimezone

from VideoHosting.additional_functions import time_since_upload
from app_api.internal_api import *
from users.models import History, Likes, Dislikes


def index(request):
    popular_videos = JsonUnpacker(get_most_popular_videos(10))
    new_videos = JsonUnpacker(get_new_videos(50))
    for i in popular_videos:
        i["video"]["date"] = time_since_upload(i["video"]["date"])
    for i in new_videos:
        i["video"]["date"] = time_since_upload(i["video"]["date"])
    return render(request, 'basic_pages/main_page.html', {"popular": popular_videos, "new_videos": new_videos})


def video_watch(request, id_video):
    try:
        video_data = JsonUnpacker(get_video(id_video, True))
        comments = JsonUnpacker(get_comments(id_video))
        for i in comments:
            i["comment"]["date"] = datetime.fromisoformat(i["comment"]["date"].replace("Z", "+00:00")).strftime(
                "%d/%m/%Y %H:%M:%S")
        video_data["comments"] = comments

        if request.user.is_authenticated:
            try:
                video_data["like"] = Likes.objects.get(username=request.user, video_id=id_video)
            except Likes.DoesNotExist:
                pass

            try:
                video_data["dislike"] = Dislikes.objects.get(username=request.user, video_id=id_video)
            except Dislikes.DoesNotExist:
                pass
            try:
                history = History.objects.get(username=request.user, video_id=id_video)
                history.date = djtimezone.now()
            except History.DoesNotExist:
                history = History(username=request.user, video_id=id_video)
            history.save()

        return render(request, "basic_pages/video.html", video_data)
    except Exception as e:
        return render(request, "users/Error.html", {"message": "Видео не найдено."})


def all_video(request):
    try:
        videos = JsonUnpacker(get_all_videos())
        for i in videos:
            i["video"]["date"] = time_since_upload(i["video"]["date"])

        return render(request, "basic_pages/all_videos.html", {"videos": videos})
    except Exception as e:
        print(e)
        return render(request, "users/Error.html", {"message": "Видео не найдено."})


def all_users(request):
    try:
        users = JsonUnpacker(get_all_users())
        return render(request, "basic_pages/all_users.html", {"users": users})
    except Exception as e:
        print(e)
        return render(request, "users/Error.html", {"message": "Что-то пошло не так"})
